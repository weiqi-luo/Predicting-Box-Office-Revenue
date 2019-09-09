<template>
  <div>
    <div style="max-widht: 50%">
      <youtube :video-id="this.videoID"></youtube>
    </div>
    <h3>Relative cast contributions</h3>
    <div v-for="(contribution, index) in contributions" :key="index" class="row mb-1">
      <div class="col-sm-2" :key="contribution.artist">{{ contribution.artist }}:</div>
      <div class="col-sm-10 pt-1">
        <b-progress :value="contribution.value" variant="info" :key="contribution.artist"></b-progress>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'YoutubeWithBars',
  props: {
    videoID: String,
    contributions: Object
  },
  data() {
      return {
      }
    },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
