<template>
  <DropZone ref="dropZone" @file-chosen="handleFileChosen" @animation-done="nextPage" />
  <div @click="showPrivacyStatement = true" class="privacy-statement">
    Privacy Statement
  </div>
  <Dialog
      v-model:visible="showPrivacyStatement"
      modal
      dismissableMask
      header="Privacy Statement"
      :draggable="false"
      :style="{ width: '50rem' }"
      :breakpoints="{ '1199px': '75vw', '575px': '90vw' }">
    <p>
      Images are stored for 2 hours by default.
      After 2 hours, every reference to the image (the file itself, and this tool's output) will be removed.
      Extending the lifetime of an image will cause it to be available for 7 days (from uploading the image).
      A link to an image (/detail/[uuid]) is always accessible to everyone, so feel free to share the link.
    </p>
</Dialog>
</template>

<script setup lang="ts">
import router from '@/router';
import Dialog from 'primevue/dialog';
import DropZone from '@/components/DropZone.vue';
import {ref} from 'vue';
import {useAppStore} from "@/store/app.ts";
import {createUpload, finalizeUpload} from "@/api.ts";

const store = useAppStore();

const dropZone = ref();

const inputNeeded = ref(true);
const showPrivacyStatement = ref(false);


async function handleFileChosen(file: File) {
  try {
    await fileChosen(file);
  } catch (e) {
    dropZone.value.showError(e.message);
    console.error(e);
  }
}

async function fileChosen(file: File) {
  inputNeeded.value = false;
  const upload = await createUpload({
    file_name: file.name,
    content_type: file.type,
  });

  store.assetFile = {
    id: upload.id,
    name: file.name,

     // not available yet
    url: "",
    is_extended: false,
    expires_at: "",
  }

  store.assetUpload = fetch(upload.url, {method: "PUT", body: file})
      .then(() => finalizeUpload(upload.id));
}

function nextPage() {
  router.push(({name: 'detail', params: {id: store.assetFile!.id}}))
}

</script>

<style scoped>
  .privacy-statement {
    position: fixed;
    bottom: 8px;
    right: 8px;
    cursor: pointer;
    font-size: 14px;
    color: #f1f1ff;
  }
</style>
