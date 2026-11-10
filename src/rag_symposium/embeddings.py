"""Turn text into vectors so search can match meaning, not only shared words.

An embedding model maps a piece of text to a list of numbers (a vector).
Texts about similar things get vectors pointing in similar directions, so
"rescinded" and "revoked" can land near each other even though they share no
words. Records and questions must go through the same model; vectors from two
different models can't be compared.

The default model, potion-base-8M, is a static embedding model: it looks up a
vector for each word piece and averages them, with no neural network running
at search time. It is about 30 MB and embeds thousands of pages in under a
second on a laptop CPU. A copy ships in this repo under models/, so hybrid
search works with no download; RAG_EMBED_MODEL or --embed-model can name another
local folder or a Hugging Face model instead.
"""
import os
import sys
from pathlib import Path

import numpy as np

HUB_MODEL = "minishlab/potion-base-8M"
# The copy in the repo: src/rag_symposium/embeddings.py -> repo root -> models/.
BUNDLED_MODEL = Path(__file__).resolve().parents[2] / "models" / "potion-base-8M"
# Use the bundled copy when it is there; otherwise fall back to downloading it.
DEFAULT_MODEL = str(BUNDLED_MODEL) if (BUNDLED_MODEL / "model.safetensors").exists() else HUB_MODEL


class Embedder:
    """Load the model once, on first use, and return unit-length vectors."""

    def __init__(self, name: str | None = None):
        self.name = name or os.environ.get("RAG_EMBED_MODEL", DEFAULT_MODEL)
        self._model = None

    def encode(self, texts: list[str]) -> np.ndarray:
        """One row per text. Rows have length 1, so a dot product is cosine similarity."""
        if self._model is None:
            # Imported here so keyword and bm25 modes never load the library.
            from model2vec import StaticModel
            print(f"Loading embedding model {self.name}", file=sys.stderr)
            self._model = StaticModel.from_pretrained(self.name)
        vectors = np.asarray(self._model.encode(texts), dtype=np.float32)
        return vectors / (np.linalg.norm(vectors, axis=1, keepdims=True) + 1e-12)
