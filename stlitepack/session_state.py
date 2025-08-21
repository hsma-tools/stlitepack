# stlite_session_state.py

# THIS HAS BEEN WRITTEN PRIMARILY BY CHATGPT-5

def _get_session_state_shim_code():
    return """
import streamlit as st

try:
    import js
    try:
        _JSROOT = js.globalThis  # usually the right entrypoint
    except AttributeError:
        _JSROOT = js
    # Try to access sessionStorage
    _STORAGE = getattr(_JSROOT, "sessionStorage", None)
except ImportError:
    # Not in Stlite/Pyodide at all
    _STORAGE = None


class SessionStateShim:
    '''
    Drop-in replacement for st.session_state in Stlite.
    Uses browser sessionStorage if available, else falls back to in-memory dict.
    '''

    def __init__(self):
        self._data = {}
        self._load()

    # ---------- Persistence ----------
    def _load(self):
        if _STORAGE is not None:
            try:
                raw = _STORAGE.getItem("stlite_session_state")
                if raw:
                    import json
                    self._data.update(json.loads(raw))
            except Exception:
                pass

    def _save(self):
        if _STORAGE is not None:
            try:
                import json
                _STORAGE.setItem("stlite_session_state", json.dumps(self._data))
            except Exception:
                pass

    # ---------- Dict-style ----------
    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value
        self._save()

    def __delitem__(self, key):
        del self._data[key]
        self._save()

    def __contains__(self, key):
        return key in self._data

    # ---------- Attribute-style ----------
    def __getattr__(self, key):
        if key in self._data:
            return self._data[key]
        raise AttributeError(key)

    def __setattr__(self, key, value):
        if key.startswith("_"):
            super().__setattr__(key, value)
        else:
            self._data[key] = value
            self._save()

    # ---------- Helpers ----------
    def get(self, key, default=None):
        return self._data.get(key, default)

    def setdefault(self, key, default=None):
        if key not in self._data:
            self._data[key] = default
            self._save()
        return self._data[key]

    def keys(self):
        return self._data.keys()

    def items(self):
        return self._data.items()

    def values(self):
        return self._data.values()

    def update(self, *args, **kwargs):
        self._data.update(*args, **kwargs)
        self._save()

    def clear(self):
        self._data.clear()
        self._save()

    def __repr__(self):
        return f"SessionStateShim({self._data})"


# Patch into Streamlit
if not isinstance(getattr(st, "session_state", None), SessionStateShim):
    st.session_state = SessionStateShim()

"""
