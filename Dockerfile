FROM python:3.11

WORKDIR /app

RUN apt-get update -o Acquire::Retries=5 && \
    apt-get install -y --no-install-recommends --fix-missing \
    ffmpeg \
    pkg-config \
    gcc \
    g++ \
    python3-dev \
    cython3 \
    patchelf \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libavfilter-dev \
    libswscale-dev \
    libswresample-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

RUN python - <<'PY'
import glob
import os

patterns = [
    "/usr/local/lib/python3.11/site-packages/ctranslate2.libs/libctranslate2*.so*",
    "/usr/local/lib/python3.11/site-packages/ctranslate2/libctranslate2*.so*",
]

paths = []
for pattern in patterns:
    paths.extend(glob.glob(pattern))

print("Found ctranslate2 libs:")
for p in paths:
    print(" -", p)

if not paths:
    print("No matching ctranslate2 shared libraries found.")

for p in paths:
    code = os.system(f'patchelf --clear-execstack "{p}"')
    print(f"patched {p}: exit={code}")
PY

RUN python - <<'PY'
try:
    import ctranslate2
    print("ctranslate2 import OK")
except Exception as e:
    print("ctranslate2 import FAILED:", repr(e))
    raise
PY

COPY . .