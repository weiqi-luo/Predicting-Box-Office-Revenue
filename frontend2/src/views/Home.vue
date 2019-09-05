<template>
  <div>
    <!--
    <b-form-input v-model="status" ></b-form-input>
    -->

    <b-row v-if="this.status === 'START'">
      <b-col>
        <b-form-group>
          <b-form-input id="input-1" v-model="IMDbInput"  @update="verify_IMDb_ID" :state ="this.IMDB_state"  placeholder= 'IBDb ID'></b-form-input>
          <b-form-input id="input-2" v-model="YTInput" @update="verify_YT_URL" :state="this.YT_state" placeholder= 'YouTube URL'></b-form-input>
          <b-button @click="mainButtonPressed">Guesstimate!</b-button>
        </b-form-group>
      </b-col>
  </b-row>
  <b-button v-if="!(this.status === 'START')" @click="status = 'START'; mode = 'nothing'; API_STATE={}" block>Restart</b-button>
<div v-if="this.mode == 'processing'">
  <h4 variant = "success"> Thinking... </h4>
  <b-spinner style="width: 3rem; height: 3rem;" label="Large Spinner" type="grow" variant = 'success'></b-spinner>
</div>
<br>
<br>
  <b-row>
    <b-col v-if="this.status === 'IMDB' || this.status === 'BOTH'">
      <MovieMetaData :data = 'this.API_STATE.metadata'></MovieMetaData>
    </b-col>
    <b-col  v-if="this.status === 'YT' || this.status === 'BOTH'">
      <YoutubeWithBars :videoID = "this.request.YT" :contributions = 'this.API_STATE.youtube'> </YoutubeWithBars>
    </b-col>
  </b-row>
  <br>
  <b-row v-if="this.mode != 'nothing'">
    <b-col>
    <h2> Results </h2>
    <br>
<div v-if="this.status === 'IMDB' || this.status === 'BOTH'" style="font-size: large;">

Diego thinks: {{this.API_STATE.results.diego}}
<br>
Venkatesh thinks: {{this.API_STATE.results.venkatesh}}
<br>
Nikos thinks: {{this.API_STATE.results.nikos}}
<br>
</div>
<div v-if="this.status === 'YT' || this.status === 'BOTH'" style = "font-size: large;">
Tim and Weiqi think: {{this.API_STATE.results.video}}
</div>
</b-col>
  </b-row>
  <br>
  </div>
</template>



<script>
import axios from 'axios'
import getYouTubeID from 'get-youtube-id'
import YoutubeWithBars from '@/components/YoutubeWithBars.vue'
import MovieMetaData from '@/components/MovieMetaData.vue'
// @ is an alias to /src

export default {
  name: 'Home',
  components: {
    YoutubeWithBars,
    MovieMetaData
  },
  data()
  {
    return {
    status: "START",
    mode: "nothing",
    IMDbInput: "",
    IMDB_state: "",
    YTInput: "",
    YT_state: "",
    request: {},
    API_STATE: {},
    API_token: ""
  }
},
methods:{
  verify_IMDb_ID(id) {
    if (id == "") {
      this.IMDB_state = "";
      return false;
    }
    else{
    var IMDb_pattern = new RegExp("tt\\d{7,8}$");
    var result = IMDb_pattern.test(id);
    this.IMDB_state = result;
    return result;
  }
  },
  verify_YT_URL(URL) {
    if (URL == "" ){
      this.YT_state = ""
      return false
      }
    else {
      var result = getYouTubeID(URL) !== null
      this.YT_state = result
      return result
  }
  },
  mainButtonPressed() {
    var IMDbInput = this.IMDbInput
    var YTInput = this.YTInput

    var id_ver = this.verify_IMDb_ID(IMDbInput)
    var yt_ver = this.verify_YT_URL(YTInput)
    var status = ""

    if (id_ver && !yt_ver) {status = "IMDB"}
    else if (!id_ver && yt_ver) {status = "YT"}
    else if (id_ver && yt_ver) {status = "BOTH"}
    else {status = "START"}

    var request = {}
    request.TYPE = status
    if (status === "IMDB" || status ==="BOTH") {request.IMDB = IMDbInput}
    if (status === "YT" || status ==="BOTH") {request.YT = getYouTubeID(YTInput)}
    if (status === "YT") { request.IMD =""}
    if (status === "IMDB") { request.YT =""}


    //console.log(request)
    this.status = status
    this.request = request

    this.postToBackend(request)
  },
  postToBackend (data_to_push) {
    console.log(data_to_push)
    var bodyFormData = new FormData();
    bodyFormData.set('TYPE', data_to_push.TYPE);
    bodyFormData.set('IMDB', data_to_push.IMDB);
    bodyFormData.set('YT', data_to_push.YT);

    const path = 'http://'+location.hostname+':80/api'
    axios.post(path, bodyFormData)
    .then(response => {
      this.API_token = response.data
      console.log(response.data)
      this.mode = "processing"
    })
    .catch(error => {
      console.log(error)
    })
  },
  requestUpdate(){
    if(this.status != "START" && this.mode =='processing'){
      console.log('update!')
      const path = 'http://'+location.hostname+':80/api/'
      axios.get(path+this.API_token)
      .then(response => {
        this.API_STATE = response.data
        console.log(response.data)
        if(response.data.done == true){
          this.mode = "results"
        }
      })
      .catch(error => {
        console.log(error)
      })
    }
  }
},
mounted(){
  setInterval(this.requestUpdate, 500);
}
}
</script>
