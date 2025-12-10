import { useState } from "react";
import { importGoogleDriveFolder, fetchImages } from "./api";

function App() {
  const [folderUrl, setFolderUrl] = useState("");
  const [isImporting, setIsImporting] = useState(false);
  const [importMessage, setImportMessage] = useState("");
  const [images, setImages] = useState([]);
  const [loadingImages, setLoadingImages] = useState(false);
  const [error, setError] = useState("");
  const [hasLoadedImages, setHasLoadedImages] = useState(false);

  const loadImages = async () => {
    try {
      setLoadingImages(true);
      setError("");
      const data = await fetchImages();
      setImages(data);
      setHasLoadedImages(true);
    } catch (err) {
      setError(err.message || "Failed to load images");
    } finally {
      setLoadingImages(false);
    }
  };

  const handleImport = async (e) => {
    e.preventDefault();
    if (!folderUrl.trim()) {
      setError("Please enter a Google Drive folder URL");
      return;
    }

    try {
      setIsImporting(true);
      setError("");
      setImportMessage("");

      const res = await importGoogleDriveFolder(folderUrl);

      setImportMessage(
        `Import started for folder ID: ${res.folder_id}. Job ID: ${res.job_id}`
      );
    } catch (err) {
      setError(err.message || "Import failed");
    } finally {
      setIsImporting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex justify-center px-4 py-6">
      <div className="w-full max-w-6xl bg-slate-950/80 border border-slate-800 rounded-3xl shadow-2xl p-6 sm:p-8">
        {/* Header */}
        <header className="mb-6 sm:mb-8">
          <h1 className="text-2xl sm:text-3xl font-semibold tracking-tight">
            Google Drive Image Importer
          </h1>
          <p className="mt-2 text-sm sm:text-base text-slate-400 max-w-2xl">
            Paste a public Google Drive folder URL containing images. The backend
            will scan the folder and store image metadata. Then you can view them
            below.
          </p>
        </header>

        {/* Form */}
        <form
          onSubmit={handleImport}
          className="space-y-3 mb-6 sm:mb-8"
        >
          <label className="block text-xs font-medium uppercase tracking-wide text-slate-400">
            Google Drive Folder URL
          </label>

          <input
            type="text"
            value={folderUrl}
            onChange={(e) => setFolderUrl(e.target.value)}
            placeholder="https://drive.google.com/drive/folders/..."
            className="w-full rounded-xl border border-slate-700 bg-slate-900/60 px-3 py-2.5 text-sm sm:text-base text-slate-100 placeholder:text-slate-500 outline-none focus:ring-2 focus:ring-emerald-500 focus:border-emerald-500 transition"
          />

          <div className="flex flex-col sm:flex-row gap-3 pt-1">
            <button
              type="submit"
              disabled={isImporting}
              className={`inline-flex items-center justify-center rounded-full px-4 py-2.5 text-sm font-semibold transition
              ${
                isImporting
                  ? "bg-emerald-700/60 text-emerald-100 cursor-not-allowed"
                  : "bg-emerald-500 text-slate-950 hover:bg-emerald-400"
              }`}
            >
              {isImporting ? "Importing..." : "Import Folder"}
            </button>

            <button
              type="button"
              onClick={loadImages}
              disabled={loadingImages}
              className={`inline-flex items-center justify-center rounded-full px-4 py-2.5 text-sm font-medium border transition
              ${
                loadingImages
                  ? "border-slate-700 text-slate-400 cursor-not-allowed"
                  : "border-slate-600 text-slate-100 hover:bg-slate-900/80"
              }`}
            >
              {loadingImages ? "Loading..." : "Show Images"}
            </button>
          </div>
        </form>

        {/* Alerts */}
        {error && (
          <div className="mb-4 rounded-xl border border-red-500/50 bg-red-900/40 px-4 py-3 text-sm text-red-100">
            {error}
          </div>
        )}

        {importMessage && (
          <div className="mb-4 rounded-xl border border-emerald-500/40 bg-emerald-900/30 px-4 py-3 text-sm text-emerald-100">
            {importMessage}
          </div>
        )}

        {/* Images Table */}
        {hasLoadedImages && (
          <section className="space-y-3">
            <div className="flex items-center justify-between gap-2">
              <h2 className="text-lg sm:text-xl font-semibold">
                Imported Images{" "}
                <span className="text-sm font-normal text-slate-400">
                  ({images.length})
                </span>
              </h2>
            </div>

            {images.length === 0 ? (
              <p className="text-sm text-slate-400">
                No images found. Try importing a folder and then click{" "}
                <span className="font-medium text-slate-200">Show Images</span>.
              </p>
            ) : (
              <div className="rounded-2xl border border-slate-800 bg-slate-950/60 overflow-hidden">
                <div className="max-h-[60vh] overflow-auto">
                  <table className="min-w-full text-sm">
                    <thead className="bg-slate-950/90 sticky top-0 z-10">
                      <tr>
                        <th className="px-3 py-2 text-left font-medium text-slate-400 border-b border-slate-800">
                          ID
                        </th>
                        <th className="px-3 py-2 text-left font-medium text-slate-400 border-b border-slate-800">
                          Name
                        </th>
                        <th className="px-3 py-2 text-left font-medium text-slate-400 border-b border-slate-800">
                          Google Drive ID
                        </th>
                        <th className="px-3 py-2 text-left font-medium text-slate-400 border-b border-slate-800">
                          MIME Type
                        </th>
                        <th className="px-3 py-2 text-left font-medium text-slate-400 border-b border-slate-800">
                          Size (KB)
                        </th>
                        <th className="px-3 py-2 text-left font-medium text-slate-400 border-b border-slate-800">
                          Destination URL
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {images.map((img) => (
                        <tr
                          key={img.id}
                          className="odd:bg-slate-900/40 even:bg-slate-900/10 hover:bg-slate-800/20 transition"
                        >
                          <td className="px-3 py-2 text-slate-500 border-b border-slate-900/60">
                            {img.id}
                          </td>
                          <td className="px-3 py-2 border-b border-slate-900/60">
                            <span className="block truncate max-w-[150px] sm:max-w-xs" title={img.name}>
                              {img.name}
                            </span>
                          </td>
                          <td className="px-3 py-2 font-mono text-xs text-slate-400 border-b border-slate-900/60">
                            <span className="block truncate max-w-[100px]" title={img.google_drive_id}>
                              {img.google_drive_id}
                            </span>
                          </td>
                          <td className="px-3 py-2 text-slate-400 border-b border-slate-900/60">
                            {img.mime_type}
                          </td>
                          <td className="px-3 py-2 text-slate-400 border-b border-slate-900/60">
                            {img.size ? Math.round(img.size / 1024) : "-"}
                          </td>
                          <td className="px-3 py-2 border-b border-slate-900/60">
                            <a
                              href={img.storage_path}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="text-emerald-400 hover:text-emerald-300 hover:underline block truncate max-w-[180px]"
                              title={img.storage_path}
                            >
                              {img.storage_path}
                            </a>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </section>
        )}
      </div>
    </div>
  );
}

export default App;