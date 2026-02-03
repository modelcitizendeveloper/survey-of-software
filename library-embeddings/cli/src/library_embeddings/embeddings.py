"""Core embeddings functionality."""

from pathlib import Path
from typing import List, Tuple, Optional
from gensim.models import Word2Vec
import json


class LibraryEmbeddings:
    """Wrapper for library embeddings model."""

    def __init__(self, model_path: Optional[Path] = None):
        """
        Load embeddings model.

        Args:
            model_path: Path to gensim Word2Vec model. If None, uses bundled model.
        """
        if model_path is None:
            # Use bundled 100d model
            data_dir = Path(__file__).parent / "data"
            model_path = data_dir / "embeddings_100d.model"

        if not model_path.exists():
            raise FileNotFoundError(
                f"Model not found at {model_path}. "
                "Download from: https://github.com/modelcitizendeveloper/library-embeddings"
            )

        self.model = Word2Vec.load(str(model_path))
        self.vocab = set(self.model.wv.index_to_key)

    def similar(self, library: str, topn: int = 10) -> List[Tuple[str, float]]:
        """
        Find libraries similar to the given library.

        Args:
            library: Library name (e.g., 'pandas', 'flask')
            topn: Number of results to return

        Returns:
            List of (library_name, similarity_score) tuples
        """
        if library not in self.vocab:
            raise ValueError(
                f"'{library}' not in vocabulary. "
                f"Available libraries: {len(self.vocab)} total. "
                "Try: similar('pandas') or similar('flask')"
            )

        return self.model.wv.most_similar(library, topn=topn)

    def analogy(
        self,
        positive: List[str],
        negative: List[str],
        topn: int = 5
    ) -> List[Tuple[str, float]]:
        """
        Perform vector arithmetic: positive - negative.

        Example: flask - threading + asyncio = ?

        Args:
            positive: Libraries to add (e.g., ['flask', 'asyncio'])
            negative: Libraries to subtract (e.g., ['threading'])
            topn: Number of results

        Returns:
            List of (library_name, similarity_score) tuples
        """
        missing = [lib for lib in positive + negative if lib not in self.vocab]
        if missing:
            raise ValueError(f"Not in vocabulary: {missing}")

        return self.model.wv.most_similar(
            positive=positive,
            negative=negative,
            topn=topn
        )

    def cluster_analysis(self, library: str, topn: int = 20) -> dict:
        """
        Analyze ecosystem cluster for a library.

        Args:
            library: Library to analyze
            topn: Number of similar libraries to include

        Returns:
            Dict with cluster info, similar libraries, metadata
        """
        if library not in self.vocab:
            raise ValueError(f"'{library}' not in vocabulary")

        similar = self.similar(library, topn=topn)

        # Infer cluster from similar libraries
        cluster = {
            'library': library,
            'similar_libraries': similar,
            'cluster_size': len(similar),
            'avg_similarity': sum(score for _, score in similar) / len(similar)
        }

        return cluster

    def search(self, query: str, topn: int = 10) -> List[Tuple[str, float]]:
        """
        Fuzzy search for libraries matching query string.

        Args:
            query: Search string
            topn: Number of results

        Returns:
            Libraries with names containing query string
        """
        query_lower = query.lower()
        matches = [
            (lib, 1.0) for lib in self.vocab
            if query_lower in lib.lower()
        ]

        # Sort by relevance (exact match first, then shorter names)
        matches.sort(key=lambda x: (
            x[0].lower() != query_lower,  # Exact match first
            len(x[0]),  # Shorter names first
            x[0]  # Alphabetical
        ))

        return matches[:topn]

    def info(self) -> dict:
        """Get model metadata."""
        return {
            'vocabulary_size': len(self.vocab),
            'dimensions': self.model.wv.vector_size,
            'sample_libraries': sorted(list(self.vocab))[:20]
        }
