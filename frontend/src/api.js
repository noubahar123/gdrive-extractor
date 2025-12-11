const API_BASE_URL = "https://heartfelt-comfort-production-74d5.up.railway.app/api/v1"                 
//  "http://127.0.0.1:8000/api/v1";   

export async function importGoogleDriveFolder(folderUrl) {
  const res = await fetch(`${API_BASE_URL}/import/google-drive`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ folder_url: folderUrl }),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to start import");
  }

  return res.json();
}

export async function fetchImages() {
  const res = await fetch(`${API_BASE_URL}/images`);
  if (!res.ok) {
    throw new Error("Failed to fetch images");
  }
  return res.json();
}
