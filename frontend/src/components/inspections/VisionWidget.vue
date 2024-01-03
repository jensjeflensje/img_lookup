<template>
  <div v-if="loading">
    Loading...
  </div>
  <div v-else class="widget-content">
    <div class="vision-row">
      <div id="src-image">
        <img ref="srcImage" :src="props.assetUrl" alt="">

        <div
            v-if="!imageLoading && drawPoints"
            v-for="word in data.words"
            class="inspection-point"
            :style="absoluteToRelative(word.vertices)"
        >
          <span @click.prevent="showPointDetail(word)">
            <span class="inspection-icon">🔍</span>
          </span>
        </div>
        <div>
          <input v-model="drawPoints" type="checkbox"> Show points on image
        </div>
      </div>
      <div>
        <div class="current-point">
          <h3>🔍 Text</h3>
          <div v-if="currentPoint">
            <p>
              Text: {{ currentPoint.text }}
              Language: {{ currentPoint.language_name }} ({{ currentPoint.language_code }})
            </p>
            <p><a target="_blank" :href="`https://google.com/search?q=${currentPoint.text}`">Search on Google</a></p>
          </div>
          <span v-else>Click on a point on the image to see info</span>
        </div>
      </div>
      <div v-if="data.landmarks.length > 0" class="vision-data-list">
        <h3>Landmarks</h3>
        <ul class="string-list">
          <li v-for="landmark in data.landmarks">{{ landmark.name }}</li>
        </ul>
      </div>
      <div v-if="data.keywords.length > 0" class="vision-data-list">
        <h3>Keywords</h3>
        <ul class="string-list">
          <li v-for="keyword in data.keywords">{{ keyword }}</li>
        </ul>
      </div>
      <div v-if="data.labels.length > 0" class="vision-data-list">
        <h3>Labels</h3>
        <ul class="string-list">
          <li v-for="label in data.labels">{{ label }}</li>
        </ul>
      </div>
      <div v-if="data.pages.length > 0" class="vision-data-list">
        <h3>Pages</h3>
        <ul class="string-list">
          <li v-for="page in data.pages"><a :href="page.url">{{ page.name }}</a></li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {fetchInspection} from "@/api.ts";
import {nextTick, reactive, ref} from "vue";

import VisionInspection, {
  VisionInspectionWord, VisionInspectionBoundingBoxVertice,
} from "@/types/inspections/VisionInspection.ts";

const props = defineProps({
  assetId: {
    required: true,
    type: String,
  },
  assetUrl: {
    required: true,
    type: String,
  },
});

const loading = ref(true);
const imageLoading = ref(true);

const drawPoints = ref(true);

const srcImage = ref<HTMLImageElement>();
const currentPoint = ref<VisionInspectionWord>();

const data = reactive({}) as VisionInspection;

/**
 * Convert absolute image coordinates to relative ones (scaled image)
 */
function absoluteToRelative(vertices: VisionInspectionBoundingBoxVertice[]) {
  const allX = vertices.map(vertice => vertice.x);
  const allY = vertices.map(vertice => vertice.y);

  // center of the bounding box (divided by 2 because of Google?)
  const avgX = allX.reduce((a, b) => a + b) / allX.length;
  const avgY = allY.reduce((a, b) => a + b) / allY.length;

  const absoluteWidth = srcImage.value!.naturalWidth;
  const absoluteHeight = srcImage.value!.naturalHeight;
  const virtualWidth = srcImage.value!.clientWidth;
  const virtualHeight = srcImage.value!.clientHeight;

  return { // using right and bottom, not left and top
    // minus a few to not put the magnifying glass over everything
    left: Math.round(avgX / absoluteWidth * virtualWidth) + 'px',
    top: Math.round(avgY / absoluteHeight * virtualHeight) + 'px',
  };
}

function showPointDetail(point: VisionInspectionWord) {
  currentPoint.value = point;
}

async function fetchData() {
  const inspection = await fetchInspection(props.assetId, "vision") as VisionInspection;
  data.pages = inspection.pages;
  data.words = inspection.words;
  data.labels = inspection.labels;
  data.keywords = inspection.keywords;
  data.landmarks = inspection.landmarks;
  loading.value = false;
  nextTick(() => srcImage.value!.onload = () => imageLoading.value = false);
}
fetchData();
</script>


<style scoped>
  .widget-content {
    text-align: left;
  }

  .vision-row {
    margin: 0 auto;
    padding: 0 10px;
    max-width: 1600px;
    width: 100%;
    display: flex;
    flex-wrap: wrap;
    align-items: flex-start;
    gap: 26px;
  }

  #src-image {
    position: relative;
  }

  #src-image > img {
    max-height: 500px;
    max-width: 500px;
  }

  .inspection-point {
    position: absolute;
    cursor: pointer;
    transition: transform 300ms;
  }

  .inspection-point:hover {
    transform: scale(1.2);
  }

  .inspection-point > span {
    font-size: 18px;
  }

  .inspection-icon {
    font-size: 24px;
    text-shadow: 0 0 3px #000;
  }

  .current-point {
    text-align: left;
    max-width: 150px;
  }

  .string-list {
    text-align: left;
    list-style: none;
    padding-left: 0;
  }

  .vision-data-list {
    max-width: 200px;
  }
</style>