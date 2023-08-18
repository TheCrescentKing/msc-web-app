<template>
	<div class="granule-info">
		<dl>
			<dt>Granule Name</dt>
			<dd>
				{{ granule.name }}
			</dd>
			<dt>Cloud cover</dt>
			<dd>
				{{ granule.cloud_cover }}
			</dd>
		</dl>
		<button v-if="!granule.isDownloaded" @click="download">Download</button>
		<div v-else>
			<button @click="viewMineralMap">View mineral map</button>
		</div>
		<PlotData v-if="showPlot" :plot-data="plotData" @close="closePlot" />
	</div>
</template>

<script>
import PlotData from "./PlotData.vue";

export default {
	components: {
		PlotData,
	},

	props: {
		granule: {
			type: Object,
			required: true,
		},
	},

	data() {
		return {
			plotData: {},
			showPlot: false,
			isDownloading: false,
		};
	},

	methods: {
		download() {
			this.isDownloading = true;
			httpClient
				.post("download", {
					name: this.granule.name,
					url: this.granule.asset_url,
				})
				.then((res) => {
					this.$emit("granule-downloaded", this.granule);
					this.isDownloading = false;
				});
			// console.log(this.granule.asset_url);
		},
		viewMineralMap() {
			const urlSafe = this.granule.name.replace(".nc", "");
			httpClient.get("mineral-map/" + urlSafe).then((res) => {
				this.plotData = res.data;
				this.showPlot = true;
			});
		},
		closePlot() {
			this.showPlot = false;
		},
	},
};
</script>

<style>
.granule-info {
	position: absolute;
	top: 1em;
	left: 1em;
	background: white;
	border-radius: 1em;
	padding: 1em;
}
</style>
