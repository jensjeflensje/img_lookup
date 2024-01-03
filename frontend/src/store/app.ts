import { defineStore } from 'pinia'
import AssetFile from "@/types/AssetFile.ts";
import InspectionsResponse from "@/types/InspectionsResponse.ts";

export const useAppStore = defineStore('app', {
  state: () => ({
    assetUpload: null as Promise<InspectionsResponse> | null,
    assetFile: null as AssetFile | null,
  }),
  actions: {},
})
