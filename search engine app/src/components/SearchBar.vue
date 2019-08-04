<template>
    <div class="container">
        <input placeholder="Search term" class="form-control input-sm" @keyup.enter="trigger_click" autofocus v-model="query" id="search_text" type="text">
        <br>
        <button class="btn btn-light" type="submit" @click="search_clicked" ref="button_search">Search</button>
        <br>      
        <br>       
        <div v-if="showResult && result.length == 0">
            Nothing to show, No results.
        </div>
        <h4 v-else-if="showResult">
            {{result[0].count}} results:
        </h4>        
        <div v-for="(v, index) in result" :key="v.title" >
            <a :href="v.url" target="_blank">{{index + 1}} - {{v.title}}</a>         
        </div>
    </div>       
</template>

<script>
export default {
  mounted(){
      this.showResult = false;
  },
  methods: {
    set_data: function(data){
        this.result = data;
    },

    trigger_click: function(){
        this.$refs.button_search.click();
    },

    search_clicked: function(event){      
      this.showResult = true;
      let query = this.query;
      let url = `http://localhost:3000/query/${query}`;       
      fetch(url)
        .then(
            function(response) {
                console.log(response.status);
                if (response.status !== 200) {
                    console.log(response.json);
                    return;
                } else {
                    response.json().then(function(d) {
                        console.log(d);
                        this.result = d;
                    }.bind(this));
                }
            }.bind(this)
        );
    },
  },
  data: function() {
      return {              
        showResult: false,
        query: "",
        result: []
      }
  },
}
</script>

<style>

</style>
