<template>
  <div class="content" :style="{backgroundImage: `url('${asset.url}')`}">
    <div class="inner-content">
      <h1>
        {{ asset.name }}
         <span v-if="uploadShowLoading && uploading">(⏳)</span>
      </h1>
      <p v-if="!asset.is_extended">
        An image is normally saved for 2 hours. You can extend this to 7 days by
        <a href="#" @click.prevent="extendLifetime">clicking here</a>.
      </p>
      <p v-else>
        This image will be kept until {{ formatDate(asset.expires_at) }}.
        You can share this page's link with others.
      </p>
      <div v-if="!uploading" class="inspections-container">
        <Card class="inspection-box first-box">
          <template #title>Metadata</template>
          <template #content>
            <MetadataWidget @no-place-data="reorderNoPlaceData" :asset-id="asset.id"/>
          </template>
        </Card>
        <div>
          <Card class="inspection-box inner-box">
            <template #title>Place</template>
            <template #content>
              <PlaceWidget :asset-id="asset.id"/>
            </template>
          </Card>
          <Card class="inspection-box inner-box">
            <template #title>Properties</template>
            <template #content>
              <PropertiesWidget :asset-id="asset.id"/>
            </template>
          </Card>
        </div>
        <Card class="inspection-box bigger-box" :style="{order: visionOrder}">
          <template #title>Vision</template>
          <template #content>
            <VisionWidget :asset-id="asset.id" :asset-url="asset.url" />
          </template>
        </Card>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {extendAsset, fetchAsset} from "@/api.ts";
import {useRoute} from "vue-router";
import {useAppStore} from "@/store/app.ts";
import {reactive, ref} from "vue";
import AssetFile from "@/types/AssetFile.ts";
import MetadataWidget from "@/components/inspections/MetadataWidget.vue";
import Card from 'primevue/card';
import PlaceWidget from "@/components/inspections/PlaceWidget.vue";
import VisionWidget from "@/components/inspections/VisionWidget.vue";
import PropertiesWidget from "@/components/inspections/PropertiesWidget.vue";

const route = useRoute()
const store = useAppStore();

const uploading = ref(true);
const uploadShowLoading = ref(false);

const visionOrder = ref(5);

const asset = reactive<AssetFile>({
  id: store.assetFile?.id ?? route.params.id as string,
  name: store.assetFile?.name ?? "",

  // not possible yet (as it isn't finalized yet)
  url: "",
  is_extended: false,
  expires_at: "",
});

/**
 * Put vision widget on top, because there is no location data.
 */
function reorderNoPlaceData() {
  visionOrder.value = 1;
}

function formatDate(value: string) {
  const date = new Date(value);
  return `${date.getDate()}-${date.getMonth() + 1}-${date.getFullYear()} ${date.getHours()}:${date.getMinutes()}`
}

async function extendLifetime() {
  const extendRequest = await extendAsset(asset.id);
  asset.is_extended = extendRequest.is_extended;
  asset.expires_at = extendRequest.expires_at;
}

async function waitForUpload() {
  setTimeout(() => uploadShowLoading.value = true, 300);
  await store.assetUpload;
  const requestedAsset = await fetchAsset(route.params!.id as string);
  // just for now? Hopefully?
  asset.id = requestedAsset.id;
  asset.name = requestedAsset.file_name;
  asset.url = requestedAsset.url;
  asset.is_extended = requestedAsset.is_extended;
  asset.expires_at = requestedAsset.expires_at;

  document.title = `${asset.name} - Image Lookup`;

  uploading.value = false;
}

waitForUpload();
</script>

<style scoped>
  .inner-content {
    text-align: center;
    padding-top: 100px;
    padding-bottom: 40px;
    animation: 1s fade-in ease-in;
    position: relative;
    z-index: 11;
  }

  .content {
    background-size: cover;
    background-position: center;
    min-height: 100vh;
    padding: 0 24px;
  }

  .content::before {
    content: '';
    background: rgb(21,21,21);
    background: linear-gradient(180deg, rgba(21,21,21,0.45) 15%, rgba(21,21,21,0.65) 60%, rgba(21,21,21,0.85) 100%);
    position: fixed;
    inset: 0;
    z-index: 1;
  }

  h1 {
    color: var(--text-color);
    position: relative;
  }

  .inspections-container {
    margin: 0 auto;
    max-width: 1800px;
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    align-items: stretch;
    gap: 24px;
  }

  .inspection-box {
    max-width: 740px;
    max-height: 626px;
    width: 100%;
    order: 5;

    /* From https://css.glass */
    background: rgba(172, 172, 172, 0.24);
    border-radius: 16px;
    box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(6.4px);
    -webkit-backdrop-filter: blur(6.4px);
    border: 1px solid rgba(172, 172, 172, 0.35);
  }

  .inner-box {
    margin-bottom: 24px;
  }

  .first-box {
    order: 0;
  }

  .bigger-box {
    max-width: 1502px;
  }
</style>
