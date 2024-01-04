<template>
  <div v-if="loading">
    Loading...
  </div>
  <div v-else>
    <div class="data-table">
      <DataTable
          size="small"
          :value="Object.entries(data.data).map(([key, value]) => ({key: key, value: value}))">
        <Column class="key-column" field="key" header="Type"></Column>
        <Column field="value" header="Value"></Column>
      </DataTable>
    </div>
  </div>
</template>

<script setup lang="ts">
import {fetchInspection} from "@/api.ts";
import {reactive, ref} from "vue";

import DataTable from 'primevue/datatable';
import Column from 'primevue/column';

const props = defineProps({
  assetId: {
    required: true,
    type: String,
  },
});

const loading = ref(true);

const data = reactive({data: {}});


async function fetchData() {
  const inspection = await fetchInspection(props.assetId, "place");
  data.data = inspection;
  loading.value = false;
}
fetchData();
</script>


<style scoped>
  .data-table {
    max-height: 250px;
    overflow-y: scroll;
  }
</style>