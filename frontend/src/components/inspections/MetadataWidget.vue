<template>
  <div v-if="loading">
    Loading...
  </div>
  <div v-else>
    <div v-if="data.cleaned.latitude && data.cleaned.longitude">
      <a
          class="plain-link"
          target="_blank"
          :href="`https://www.google.com/maps?q=${data.cleaned.latitude},${data.cleaned.longitude}`"
      >
        <i class="header-icon pi pi-map"></i> {{ data.cleaned.latitude }} {{ data.cleaned.longitude }}
      </a>
    </div>
    <i v-if="data.cleaned.device" class="header-icon pi pi-camera"></i> {{ data.cleaned.device }}
    <div class="detail-container">
      <div class="exif-list">
        <DataTable
            size="small"
            :value="Object.entries(data.exif).map(([key, value]) => ({key: key, value: value}))">
          <Column class="key-column" field="key" header="Key"></Column>
          <Column class="value-column" field="value" header="Value"></Column>
        </DataTable>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {fetchInspection} from "@/api.ts";
import {reactive, ref} from "vue";
import MetadataInspection from "@/types/inspections/MetadataInspection.ts";

import DataTable from 'primevue/datatable';
import Column from 'primevue/column';

const props = defineProps({
  assetId: {
    required: true,
    type: String,
  },
});

const emit = defineEmits(['no-place-data'])

const loading = ref(true);

const data = reactive<MetadataInspection>({exif: {}, cleaned: {}});


async function fetchData() {
  const inspection = await fetchInspection(props.assetId, "metadata") as MetadataInspection;
  data.exif = inspection.exif;
  data.cleaned = inspection.cleaned;
  if (!data.cleaned.latitude || !data.cleaned.longitude) {
    emit('no-place-data')
  }
  loading.value = false;
}
fetchData();
</script>


<style scoped>
  .header-icon {
    font-size: 1rem;
  }

  .detail-container {
    margin-top: 10px;
  }

  .exif-list {
    max-height: 470px;
    overflow-y: scroll;
  }
</style>