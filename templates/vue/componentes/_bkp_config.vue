<template id="config">
  <v-form>
    <v-container class="pa-6">
      <v-row>
        <v-col cols="12" sm="6">
          <v-text-field
            value="{{request.user.username}}"
            label="Usuário"
            disabled
          ></v-text-field>
        </v-col>
        <v-col cols="12" sm="6">
        </v-col>

        <v-col cols="12" sm="6">
          <v-text-field
            value="{{request.user.first_name}} {{request.user.last_name}}"
            label="Nome Completo"
            disabled
          ></v-text-field>
        </v-col>
        <!--Area de troca de senha sua-->
        <v-col cols="6" sm="6">
          <password></password>
        </v-col>
        <!--Só irá aparecer para quem for administrador-->
        {% if request.user.is_superuser or request.user.is_staff%}
        <v-col cols="6" sm="6">
          <!--troca de senha geral-->
          <resetaluno></resetaluno>
        </v-col>
        {% endif %}
      </v-row>
    </v-container>
  </v-form>
</template>

{% include 'vue/componentes/password.vue' %}

{% include 'vue/componentes/resetaluno.vue' %}

<script>
const Componentepassword = { template: "<password></password>" };
const Componenteresetaluno = { template: "<resetaluno></resetaluno>" };

Vue.component("config", {
  template: "#config",
  delimiters: ["[[", "]]"],
  vuetify: new Vuetify(),

  data: () => ({}),
});
</script>