<template>
	<div class="plot resizer">
		<button class="plot__close-button" @click="close">Close</button>
		<iframe class="resized" ref="plotFrame" />
	</div>
</template>

<script>
export default {
	props: {
		plotData: {
			type: String,
			required: true,
		},
	},

	// data() {
	// 	return {
	// 		plotData: {},
	// 	};
	// },

	methods: {
		close() {
			this.$emit("close");
		},
	},

	mounted() {
		const iframe = this.$refs.plotFrame;
		iframe.srcdoc = this.plotData;
	},
};
</script>

<style>
.plot {
	position: absolute;
	top: 1em;
	left: 27em;
	background: white;
	border-radius: 1em;
	padding: 1em;
	width: 100%;
	height: 100%;
}

.plot__close-button {
	align-self: baseline;
}

.resizer {
	display: flex;
	margin: 0;
	padding: 0;
	resize: both;
	overflow: hidden;
}
.resizer > .resized {
	flex-grow: 1;
	margin: 0;
	padding: 0;
	border: 0;
}
</style>
