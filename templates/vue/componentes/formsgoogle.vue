<template id="formsgoogle">
<div>
  <v-card>
    <v-card-text>
      <v-row>
        <iframe src="https://www.undb.edu.br/editais" height="600" width="100%" style="border-width: 0"></iframe>
      </v-row>
    </v-card-text>
    <v-card-actions class="justify-space-between"> 
    </v-card-actions>
  </v-card>
  </div>  
</template>
<script>
Vue.component('formsgoogle', {
  template: '#formsgoogle',
  delimiters: ["[[", "]]"],
  vuetify: new Vuetify(),
  data: () => ({
      length: 3,
      onboarding: 0,
    }),

    methods: {
      next () {
        this.onboarding = this.onboarding + 1 === this.length
          ? 0
          : this.onboarding + 1
        console.log(error);
      },
      prev () {
        this.onboarding = this.onboarding - 1 < 0
          ? this.length - 1
          : this.onboarding - 1
          console.log(error);
      },
    },
});
</script>