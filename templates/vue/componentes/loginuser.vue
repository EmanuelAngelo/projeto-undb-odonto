<template id="loginuser">
  <v-dialog max-width="500px" v-model="dialog">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="#215f5e" :loading="loading" small depressed label dark :block="block"  class="my-1" v-bind="attrs" v-on="on">
        <v-icon dark v-if="$vuetify.breakpoint.mdAndUp" left> mdi-arrow-right </v-icon>
        [[label]]</v-btn
      >
    </template>
    <v-card>
      <v-form>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" md="5" v-if="showUsername">
                <v-text-field
                  label="Digite seu RA*"
                  required
                  placeholder="002-123456"
                  
                  outlined
                  v-model="validate.username"
                ></v-text-field>
              </v-col>
              <v-col cols="12" md="5">
                <v-text-field
                  label="Sua senha*"
                  type="password"
                  required
                  placeholder="Senha numérica"
                  outlined
                  v-model="validate.password"
                ></v-text-field>
              </v-col>

              <!--<v-col cols="12" sm="6" md="5">
                <v-text-field
                  value="A Esterelizar"
                  label="Situação"
                  disabled
                  outlined
                ></v-text-field>
              </v-col>-->
            </v-row>
          </v-container>
          <small>*Nunca passe sua senha para outra pessoa.</small>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="dialog = false">
            Voltar
          </v-btn>
          <v-btn color="blue darken-1" text :loading="loading" @click="validatePassword()" >
            Concluir
          </v-btn>
        </v-card-actions>
      </v-form>
    </v-card>
  </v-dialog>
</template>

{% url 'user:api_validate_password' as validate_password %}


<script>
Vue.component("loginuser", {
  template: "#loginuser",
  delimiters: ["[[", "]]"],
  props:{
    label:{
      type: String,
      default:'Autenticar'
    },
    username:{
      type: String,
      default:''
    },
    block:{
      type: Boolean,
      default:true
    },
    showUsername:{
      type: Boolean,
      default:true
    }
  },
  data() {
    return {
      loading: false,
      dialog: false,
      validate: {
        username: null,
        password: null,
      },
      loading:false
    };
  },
  methods: {
    limparObjeto() {
      this.validate.username = '' ;
      this.validate.password = '';
    },
    validatePassword() {
      if(this.username){
        this.validate.username = this.username
      }
      if (this.validate.username && this.validate.password) {
        //console.log(this.validate.username);
        //console.log(this.validate.password);
        this.loading = true
        this.$http.post("{{validate_password}}", this.validate).then((response) => {
            //console.log(response.data);
            this.$emit("validate-password", response.data.id);
            this.dialog = false;
            this.limparObjeto();
          }).catch((error) => {
            this.$emit("validate-password", false);
            alert('Usuário e/ou Senha inválidos')
            console.log(error);
          }).finally(() => {
            // console.log("sempre executa");
            this.loading = false
           
          });
      } else {
        alert("Por favor insira RA e/ou sua SENHA");
      }
    },
  },
  mounted(){
    this.limparObjeto()
    
  },
  watch:{
    dialog(value){
     // console.log('username',this.username)
    }
  }
});
</script>
