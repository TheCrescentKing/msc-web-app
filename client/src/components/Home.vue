<template>
	<div class="container">
		<div id="map"></div>
		<!-- <granule-popup :granule="selectedGranule" v-show="false" ref="popup" /> -->
	</div>
</template>

<script>
import Map from "ol/Map.js";
import OSM from "ol/source/OSM.js";
import TileLayer from "ol/layer/Tile.js";
import View from "ol/View.js";
import Polygon from "ol/geom/Polygon.js";

import axios from "axios";
import GranulePopup from "./templates/GranulePopup.vue";
import VectorTileLayer from "ol/layer/VectorTile";
import VectorSource from "ol/source/Vector";
import Style from "ol/style/Style";
import Stroke from "ol/style/Stroke";
import Feature from "ol/Feature";
import BaseVectorLayer from "ol/layer/BaseVector";
import VectorImageLayer from "ol/layer/VectorImage";
import { fromLonLat } from "ol/proj";

export default {
	components: {
		GranulePopup,
	},
	name: "Home",
	data() {
		return {
			// map: null,
			granules: [],
			granulesLoaded: false,
			selectedGranule: {},
			zoom: 5,
		};
	},
	methods: {
		getGranules() {
			const path = "http://localhost:5001/granules";
			axios
				.get(path)
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
				// polygon.bindTooltip(granule.name);
				// polygon.bindPopup(() => this.$refs.popup.$el);
			});

			const layer = new VectorImageLayer({
				map: this.map,
				source: source,
				style: new Style({
					stroke: new Stroke({
						color: "red",
						width: 4,
					}),
				}),
			});

			// this.map.addLayer(layer);
		},
	},

	mounted() {
		this.getGranules();
		this.map = new Map({
			target: "map",
			layers: [
				new TileLayer({
					source: new OSM(),
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
					const granule = self.granules.find((g) => g.ol_uid === feature.ol_uid);
					console.log("granule:", granule);
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
