<template>
  <div v-if="loading">
    Loading...
  </div>
  <div v-else>
    <DataTable
        size="small"
        :value="Object.entries(data.hash).map(([key, value]) => ({key: key, value: value}))">
      <Column field="key" header="Algorithm"></Column>
      <Column field="value" header="Value"></Column>
    </DataTable>
  </div>
</template>

<script setup lang="ts">
import {fetchInspection} from "@/api.ts";
import {reactive, ref} from "vue";
import PropertiesInspection from "@/types/inspections/PropertiesInspection.ts";
import Column from "primevue/column";
import DataTable from "primevue/datatable";

const props = defineProps({
  assetId: {
    required: true,
    type: String,
  },
});

const loading = ref(true);

const data = reactive({}) as PropertiesInspection;


async function fetchData() {
  const inspection = await fetchInspection(props.assetId, "properties") as PropertiesInspection;
  data.height = inspection.height;
  data.width = inspection.width;
  data.hash = inspection.hash;

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