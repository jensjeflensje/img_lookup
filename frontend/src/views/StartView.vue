<template>
  <DropZone @file-chosen="fileChosen" @animation-done="nextPage" />
</template>

<script setup lang="ts">
import router from '@/router';
import DropZone from '@/components/DropZone.vue';
import {ref} from 'vue';
import {useAppStore} from "@/store/app.ts";
import {createUpload, finalizeUpload} from "@/api.ts";

const store = useAppStore();

const inputNeeded = ref(true);


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
</style>
