<template>
	<div>
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
		<button @click="download">Download</button>
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
			console.log(this.granule.asset_url);
		},
	},
};
</script>
