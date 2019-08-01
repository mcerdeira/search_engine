<template>
    <div>
        <input v-model="query" id="search_text" type="text">
        <button @click="search_clicked">Search</button>
        <br>
        <br>
        <div v-for="v in result" :key="v.title" >
            <a :href="v.url" target="_blank">{{v.title}}</a>
        </div>
    </div>    
</template>

<script>
export default {
  methods: {
    set_data: function(data){
        this.result = data;
    },

    search_clicked: function(event){
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
        query: "",
        result: [{title:"", "url":""},]
      }
  },
}
</script>

<style>

</style>
