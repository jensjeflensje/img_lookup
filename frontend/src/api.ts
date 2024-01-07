import UploadResponse from "@/types/UploadResponse.ts";
import UploadRequest from "@/types/UploadRequest.ts";
import InspectionsResponse from "@/types/InspectionsResponse.ts";
import AssetResponse from "@/types/AssetResponse.ts";

export const BASE_URL = import.meta.env.VITE_APP_URL;

export async function createUpload(req: UploadRequest) : Promise<UploadResponse> {
    const res = await fetch('/api/assets/create', {
        method: 'POST',
        body: JSON.stringify(req),
        headers: {
            'Content-Type': 'application/json',
        },
    });
    if (res.status !== 200) throw new Error("Failed to upload image")
    return await res.json();
}

export async function finalizeUpload(id: string) : Promise<InspectionsResponse> {
    const res = await fetch(`/api/assets/${id}/finalize`, {
        method: 'POST',
    });
    return await res.json();
}

export async function fetchAsset(id: string) : Promise<AssetResponse> {
    const res = await fetch(`/api/assets/${id}`);
    return await res.json();
}

export async function extendAsset(id: string) : Promise<AssetResponse> {
    const res = await fetch(`/api/assets/${id}/extend`, {
        method: 'POST',
    });
    return await res.json();
}

export async function fetchInspection(id: string, inspectionType: string) : Promise<object> {
    const res = await fetch(`/api/assets/${id}/inspections/${inspectionType}`);
    if (res.status == 200) {
        return await res.json();
    }
    return new Promise((resolve) => {
      setTimeout(async () => resolve(await fetchInspection(id, inspectionType)), 200);
    });
}
