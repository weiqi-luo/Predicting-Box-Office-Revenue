<template>
  <div>
    <h3>Movie metadata</h3>
    <div>
    <h5 style="color: red">Title</h5>
    {{data.title}}
    <br>
    <h5 style="color: red">Release date</h5>
    {{data.release_date}}
    <br>
    <h5 style="color: red">Genres</h5>
    <ul style="list-style-type:none; padding-left: 0;">
      <li v-for="value in data.genres">
        {{ value }}
      </li>
    </ul>
    <br>
    <h5 style="color: red">Cast</h5>
    <ul style="list-style-type:none; padding-left: 0;">
      <li v-for="value in data.cast">
        {{ value }}
      </li>
    </ul>
    <br>
    <h5 style="color: red">Runtime (min)</h5>
    {{data.runtime}}
  </div>
  </div>
</template>

<script>
export default {
  name: 'MovieMetaData',
  props: {
    data: Object
  },

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>

</style>
