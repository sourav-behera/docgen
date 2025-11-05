import cocoindex
import logging
import numpy as np
import os
import functools
from psycopg_pool import ConnectionPool
from pgvector.psycopg import register_vector
from numpy.typing import NDArray

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

SRC_CODE_PATH: str = "tmp"

INCLUDED_PATTERNS: list[str] = ["*.py", "*.md", "*.txt", "*.java", "*.cpp", "*.hpp", "*.c", "*.h", "*.js", "*.ts", "*.json", "*.yaml", "*.yml", "*.html", "*.css"]
EXCLUDED_PATTERNS: list[str] = ["**/node_modules/**", "**/__pycache__/**", "**/.git/**", "**/.venv/**", "**/venv/**", "**/.env/**"] 

CHUNK_SIZE: int = 1000
CHUNK_MIN_SIZE: int = 200
CHUNK_OVERLAP_SIZE: int = 200

@cocoindex.transform_flow()
def code_to_embedding(text: cocoindex.DataSlice[str]) -> cocoindex.DataSlice[NDArray[np.float32]]:
    return text.transform(
        cocoindex.functions.SentenceTransformerEmbed(
            model="sentence-transformers/all-MiniLM-L6-v2"
        )
    )

@cocoindex.flow_def(name="CodeEmbedding")
def code_embedding_flow(flow_builder: cocoindex.FlowBuilder, data_scope: cocoindex.DataScope):
    data_scope["files"] = flow_builder.add_source(
        cocoindex.sources.LocalFile(
            path=SRC_CODE_PATH,
            included_patterns=INCLUDED_PATTERNS,
            excluded_patterns=EXCLUDED_PATTERNS
        )
    )

    code_embeddings = data_scope.add_collector()

    with data_scope["files"].row() as file:
        file["language"] = file["filename"].transform(
            cocoindex.functions.DetectProgrammingLanguage()
        )
        file["chunks"] = file["content"].transform(
            cocoindex.functions.SplitRecursively(),
            language=file["language"],
            chunk_size=CHUNK_SIZE,
            min_chunk_size=CHUNK_MIN_SIZE,
            chunk_overlap=CHUNK_OVERLAP_SIZE
        )

        with file["chunks"].row() as chunk:
            chunk["embedding"] = chunk["text"].call(code_to_embedding)
            code_embeddings.collect(
                filename=file["filename"],
                location=chunk["location"],
                code=chunk["text"],
                embedding=chunk["embedding"],
                start=chunk["start"],
                end=chunk["end"]
            )

    code_embeddings.export(
        "code_embeddings",
        cocoindex.targets.Postgres(),
        primary_key_fields=["filename", "location"],
        vector_indexes=[
            cocoindex.VectorIndexDef(
                field_name="embedding",
                metric=cocoindex.VectorSimilarityMetric.COSINE_SIMILARITY,
            )
        ]
    )


@functools.cache
def connection_pool() -> ConnectionPool:
    """
    Get a connection pool to the database.
    """
    return ConnectionPool(os.environ["COCOINDEX_DATABASE_URL"])


TOP_K =2


# Declaring it as a query handler, so that you can easily run queries in CocoInsight.
@code_embedding_flow.query_handler(
    result_fields=cocoindex.QueryHandlerResultFields(
        embedding=["embedding"], score="score"
    )
)
def search(query: str) -> cocoindex.QueryOutput:
    # Get the table name, for the export target in the code_embedding_flow above.
    table_name = cocoindex.utils.get_target_default_name(
        code_embedding_flow, "code_embeddings"
    )
    # Evaluate the transform flow defined above with the input query, to get the embedding.
    query_vector = code_to_embedding.eval(query)
    # Run the query and get the results.
    with connection_pool().connection() as conn:
        register_vector(conn)
        with conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT filename, code, embedding, embedding <=> %s AS distance, start, "end"
                FROM {table_name} ORDER BY distance LIMIT %s
            """,
                (query_vector, TOP_K),
            )
            return cocoindex.QueryOutput(
                query_info=cocoindex.QueryInfo(
                    embedding=query_vector,
                    similarity_metric=cocoindex.VectorSimilarityMetric.COSINE_SIMILARITY,
                ),
                results=[
                    {
                        "filename": row[0],
                        "code": row[1],
                        "embedding": row[2],
                        "score": 1.0 - row[3],
                        "start": row[4],
                        "end": row[5],
                    }
                    for row in cur.fetchall()
                ],
            )

def run_indexer():
    logger.info("Starting code indexing process...")
    code_embedding_flow.setup(report_to_stdout=True)
    logger.info("CocoIndex initialized.")