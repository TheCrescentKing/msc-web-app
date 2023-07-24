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
		<i v-else>Downloaded</i>
	</div>
</template>

<script>
export default {
	props: {
		granule: {
			type: Object,
			required: true,
		},
	},

	methods: {
		download() {
			httpClient.post("download", {
				name: this.granule.name,
				url: this.granule.asset_url,
			});
			// console.log(this.granule.asset_url);
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
