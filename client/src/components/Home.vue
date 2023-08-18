<template>
	<div class="container">
		<div id="map"></div>
		<granule-popup
			:granule="selectedGranule"
			v-if="showGranuleInfo"
			@granule-downloaded="granuleDownloaded"
		/>
	</div>
</template>

<script>
import Map from "ol/Map.js";
import OSM from "ol/source/OSM.js";
import TileLayer from "ol/layer/Tile.js";
import View from "ol/View.js";
import Polygon from "ol/geom/Polygon.js";

import GranulePopup from "./templates/GranulePopup.vue";
import VectorSource from "ol/source/Vector";
import Style from "ol/style/Style";
import Stroke from "ol/style/Stroke";
import Feature from "ol/Feature";
import VectorImageLayer from "ol/layer/VectorImage";
import { fromLonLat } from "ol/proj";
import XYZ from "ol/source/XYZ";
import Fill from "ol/style/Fill";

const OUTLINE_STYLE = new Style({
	stroke: new Stroke({
		color: "red",
		width: 1,
	}),
});

const FILL_STYLE = new Style({
	stroke: new Stroke({
		color: "red",
		width: 1,
	}),
	fill: new Fill({
		color: "red",
	}),
});

export default {
	components: {
		GranulePopup,
	},

	name: "Home",

	data() {
		return {
			map: null,
			granules: [],
			granulesLoaded: false,
			selectedGranule: null,
			selectedFeature: null,
			zoom: 5,
		};
	},

	computed: {
		showGranuleInfo() {
			return this.selectedGranule !== null;
		},
	},

	methods: {
		getGranules() {
			httpClient
				.get("granules")
				.then((res) => {
					this.granules = res.data;
					this.granulesLoaded = true;
					this.loadGranulesIntoMap();
				})
				.catch((error) => {
					console.error(error);
				});
		},
		loadGranulesIntoMap() {
			const source = new VectorSource();

			this.granules.forEach((granule) => {
				const mapped = granule.polygon.map(function (coords) {
					return coords.map((pair) => fromLonLat(pair));
				});
				const polygon = new Polygon(mapped);
				const feature = new Feature({
					geometry: polygon,
					name: granule.name,
				});
				granule.ol_uid = feature.ol_uid;
				source.addFeature(feature);
			});

			const layer = new VectorImageLayer({
				map: this.map,
				source: source,
				style: new Style({
					stroke: new Stroke({
						color: "red",
						width: 1,
					}),
				}),
			});
		},

		granuleDownloaded(granule) {
			this.granules.find((gran) => gran.name === granule.name).isDownloaded = true;
		},
	},

	mounted() {
		this.getGranules();

		this.map = new Map({
			target: "map",
			layers: [
				new TileLayer({
					source: new XYZ({
						url:
							"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
						maxZoom: 19,
					}),
				}),
			],
			view: new View({
				center: fromLonLat([4.8, 45.77]),
				zoom: 5,
			}),
		});

		const self = this;

		this.map.on("pointermove", function (event) {
			self.map.forEachFeatureAtPixel(
				event.pixel,
				function (feature) {
					if (self.selectedFeature) {
						self.selectedFeature.setStyle(OUTLINE_STYLE);
					}
					self.selectedFeature = feature;
					self.selectedFeature.setStyle(FILL_STYLE);
					const granule = self.granules.find((g) => g.ol_uid === feature.ol_uid);
					self.selectedGranule = granule;
				},
				{
					hitTolerance: 2,
				}
			);
		});
	},
};
</script>

<style>
.container {
	height: 90vh;
}

#map {
	height: 100%;
}
</style>
