<template id="resetaluno">
    <v-dialog v-model="dialog" persistent max-width="600px">
      <template v-slot:activator="{ on, attrs }" >
        
          <v-list-item v-on="on" color="white">
              <v-list-item-avatar>
                  <v-icon>mdi-lock</v-icon>
              </v-list-item-avatar>
              
              <v-list-item-content>
                  <v-list-item-title>Token Aluno</v-list-item-title>
                  <v-list-item-subtitle></v-list-item-subtitle>
              </v-list-item-content>
              
              <v-list-item-action></v-list-item-action>
          </v-list-item>
        
      </template>
      <v-card>
        <v-card-title>
          <div class="headline">
            Redefinição de token
          </div>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row dense>
              <span class="subtitle-2">
                {{ request.user.first_name }} {{ request.user.last_name }}
              </span>
            </v-row>
            <v-row dense>
              <v-col dense cols="12" md="6">
                <v-text-field dense
                  label="Usuário*"
                  required
                  placeholder="002-010203"
                  outlined
                  :disabled="'{{request.user.is_staff }}' == 'False'"
                  v-model="user.usuario"
                  :rules="[v=> !!v||'Campo obrigatório']"
                ></v-text-field>
              </v-col>
              <v-col dense cols="12" md="6"></v-col>
              <v-col cols="6">
                <v-text-field outlined dense
                  label="Token*" 
                  type="password"
                  v-model="user.password"
                  :rules="[v=> !!v||'Campo obrigatório', v=> v.length >= 6 ||'mínimo de 6 caracteres']"
                ></v-text-field>
              </v-col>
              <v-col cols="6">
                <v-text-field outlined dense
                  v-model="user.password2"
                  label="Confirmar Token*" 
                  type="password"
                  :rules="[v=> v == user.password ||'Token não confere']"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6"> </v-col>
            </v-row>
          </v-container>
          <small><b><span class="error--text">*</span>Seu token é pessoal e intransferível</b></small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">
            Sair
          </v-btn>
          <v-btn color="blue darken-1" text 
            :disabled="!(user.password.length >= 6 && (user.password == user.password2) && user.usuario.length > 0)" 
            @click="updateToken()"
            :loading="loading"
            >
            Salvar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>
{% url 'user:update_token' as updateToken %}
<script>
Vue.component("resetaluno", {
  template: "#resetaluno",
  delimiters: ["[[", "]]"],
  vuetify: new Vuetify(),

  data: () => ({
    dialog: false,
    loading:false,
    user:{
      usuario:'',
      password:'',
      password2:'',
    },
  }),
  mounted(){
    if('{{ request.user.is_staff}}' == 'False'){
      this.user.usuario = '{{request.user.username}}'
    }
  },
  methods:{
    updateToken(){
      this.loading = true
      this.$http.post('{{updateToken}}', this.user)
        .then(response=>{
          //console.log(response)
          alert('Token atualizado com sucesso!')
          this.clearObject()
          this.dialog = false
        }).catch(error=>{
          console.error(error)
        }).finally(()=>{
          this.loading = false
        })
    },
    clearObject(){
      this.user.usuario = ''
      this.user.password = ''
      this.user.password2 = ''
    }
  },
  watch: {
    dialog(val) {
      if (!val) return;
    },
  },
});
</script>