<template id="status" >
  <div>
    <v-card-title>
      Esterilizações
      <v-divider class="mx-4" inset vertical></v-divider>
      <v-spacer></v-spacer>
      <!--field buscar-->
      <v-flex xs12 sm4 md4>
        <v-text-field
          :custom-filter="filterOnlyCapsText"
          placeholder="Nome Sobrenome e RA"
          append-icon="mdi-magnify"
          v-model="search"
          label="Buscar"
          hide-details
          single-line
          clearable
          outlined
          dense
        ></v-text-field>
      </v-flex>
    </v-card-title>
    <!--tabela-->
    <v-data-table
      class="elevation-1"
      show-expand
      sort-desc.sync="id"
      :items-per-page="10"
      :custom-filter="filterOnlyCapsText"
      :single-expand="singleExpand"
      :expanded.sync="expanded"
      :loading="loadingDepositos"
      :headers="headers"
      :items="depositos"
      :search="search"
    >
      <template v-slot:top>
        <v-row dense class="px-4">
          <v-col class="d-flex" cols="6" dense>
            <!--Button deposito-->
            <depositarcaixa @deposito-added="getDepositos()"></depositarcaixa>
          </v-col>
          <v-col cols="6" dense align="right">
         <v-flex xs12 sm8 md8>
            <!--Situações-->   
          <v-select
            :items="complete"
            :color="$vuetify.theme.themes.light.accent"
            @change="getDepositos" 
            label="Situações"
            dense
            outlined>
            </v-select>
            <!---->
          </v-flex>
          </v-col> 
        </v-row>
      </template>
      <!--Se tiver mais de um tipo de caixa aparecer botao de mostrar mais item-->
      <template v-slot:expanded-item="{ item }">
        <td colspan="5" class="pa-4">
          <v-row dense >
            <v-card outlined tile elevation="0" width="100%">
              <v-card-title>Itens do depósito: [[item.usuario.first_name]]</v-card-title>
              <!--Criando botao geral-->

                <v-card-title v-model="item.itens"> 
                  {% if request.user.is_staff %}
                  <div v-if="item.esta_aguardando_entrega">
                    <loginuser :loading="loading" 
                              :disabled="!item.esta_aguardando_entrega"
                              ref="loginuser" 
                              :username="item.usuario.username" 
                              :show-username="false"
                              label='Entregar' :block="false" 
                              @validate-password="validarEntrega($event,item.usuario, item)">
                    </loginuser> 

                  </div>

                  <div v-if="!item.esta_aguardando_entrega">
                    
                    <v-btn  small
                            :loading="loading"
                            :disabled="!item.existe_itens_pendentes"
                            depressed 
                            label
                            @click="updateDeposito( item )"
                            :color="getColor(item.itens.situacao)">
                            Avançar Status
                            <v-icon>mdi-chevron-double-right</v-icon>

                    </v-btn>
                    
                  </div>
                  
                  {% endif %}
                </v-card-title>
                          
              <!---->  
              <v-card-text>
                <div v-if="loadingDepositos"> <!-- carregamento da entrega -->
                  <v-progress-circular size="30" indeterminate></v-progress-circular>
                </div>
                <div v-else class="depositos">
                  <samp>
                    <ul>
                      <li v-for="dItem in item.itens"
                        :key="'deposito_item_' + item.id + '_' + dItem.id"
                        class="py-1">
                        <!--Botão aonde mostrar os status-->
                        <v-btn
                          :title="[[dItem.situacao]]"
                          label
                          :disabled="dItem.situacao == computedEntregue"
                          depressed
                          small
                          :color="getColor(dItem.situacao)"
                          >
                          <v-icon small>mdi-circle</v-icon> &nbsp;
                          [[dItem.situacao]]
                        </v-btn>
                        
                       <!---->
                        <strong>[[("0000000" + dItem.id).slice(-7)]] </strong>
                        [[dItem.tipo_box.tipo_volume]] -
                        [[dItem.tipo_box.nome_volume]] : [[dItem.quantidade]]
                        [[(dItem.observacoes||'').length > 0 ? '- ('+dItem.observacoes+')' : '']]

                        <div v-if="dItem.logs_item.length > 0">
                          - Atualizado para:
                        </div>
                        <div
                          style="margin-left: 20px"
                          v-for="log in dItem.logs_item"
                          :key="'log_' + dItem.id + '_' + log.id"
                        >
                          [[log.situacao]] em: [[log.get_criado_em]]
                        </div>
                      <hr style="border-top: dotted 1px;" />
                        <br>
                      </li>
                    </ul>
                  </samp>
                </div>
              </v-card-text>
            </v-card>
          </v-row>
        </td>
      </template>
      <template v-slot:item.id="{ item }">
        [[("0000000" + item.id).slice(-7)]]
      </template>
      <template v-slot:item.depositante="{ item }">
        [[item.usuario.first_name || '']] [[item.usuario.last_name || '']]
      </template>
      <template v-slot:item.usuario="{ item }">
        [[item.usuario.username]]
      </template>
      <template v-slot:item.quantidade="{ item }">
        [[item.itens.length]]
      </template>
       <template v-slot:item.get_criado_em="{ item }">
        [[item.get_criado_em]]
      </template>

      <template v-slot:item.situacao="{ item }">
        <v-chip :class="getColor(item.situacao)" dark>[[item.situacao]] </v-chip>
      </template>

      {% if request.user.is_staff %}
      <!-- look printer adm -->
      <template v-slot:item.opcoes="{ item }">
        <v-btn icon @click="imprimir(item.itens)">
          <v-icon color="info">mdi-printer</v-icon>
        </v-btn>
      </template>
      {% endif %}
    </v-data-table>
  </div>
</template>

{% url 'box:api_deposito' as getDepositos %}
{% include 'vue/componentes/depositarcaixa.vue' %}
{% include 'vue/componentes/loginuser.vue' %}

<script src="https://cdn.jsdelivr.net/npm/jsbarcode@3.11.4/dist/JsBarcode.all.min.js"></script>


<script>
Vue.component("status", {
  template: "#status",
  delimiters: ["[[", "]]"],
  data: () => ({
    toggle_exclusive: undefined,
    loading: false,
    //date: (new Date(Date.now() - (new Date()).getTimezoneOffset() * 60000)).toISOString().substr(0, 10),
    loadingDepositos: false,
    expanded: [],
    depositos: [],
    singleExpand: false,
    dialog: false,
    dialogDelete: false,
    search: "",

    complete: [
      {text: "Todos", value: "all" },
      {text: "Entregues", value: "entregue"},
      {text: "Pendentes", value: "''"},
    ],

    headers: [
      { text: "ID", align: "start", sortable: true, value: "id" },
      { text: "Depositante", align: "start", sortable: false, value: "depositante",},
      { text: "Usuário", value: "usuario", sortable: false, width:"110px"},
      { text: "Qtde", value: "quantidade", sortable: false, align:"center"},
      { text: "Data depósito", value: "criado_em", sortable: false, },
    ],
    card: [{ text: "Acões", value: "actions", sortable: false }],
  }),

  computed: {
    computedAEsterilizar() {
      return "ESTERILIZAR";
    },
    computedEsterilizando() {
      return "ESTERILIZANDO";
    },
    computedEsterilizado() {
      return "ESTERILIZADO";
    },
    computedEntregue() {
      return "ENTREGUE";
    },
  },
  watch: {},

  mounted() {
    this.initialize();
    var staff = "{{request.user.is_staff}}" == "True";
    //console.log("staff", staff);
    /*
    if (staff) {
      this.headers.push({ text: "Opções", value: "opcoes", sortable: false, });
    }*/
  },
  methods: {
    filterOnlyCapsText(value, search, item) {
      return (
        value != null &&
        (item.usuario.username.toString().toLowerCase().indexOf(search.toString().toLowerCase()) !== -1 || 
        (`${item.usuario.first_name} ${item.usuario.last_name}`).toString().toLowerCase().indexOf(search.toString().toLowerCase()) !== -1 ||
          item.usuario.last_name.toString().toLowerCase().indexOf(search.toString().toLowerCase()) !== -1 ||
          item.id.toString().toLowerCase().indexOf(search.toString().toLowerCase()) !== -1 ||
          item.usuario.email.toString().toLowerCase().indexOf(search.toString().toLowerCase()) !== -1));
    },
    validarEntrega(usuario_autenticado_id, usuario, item){
      if(usuario_autenticado_id === usuario.id){
        this.atualizarDeposito(item) //
      }else{
        alert('Liberação não autorizada')
      }
    },
    updateSituacao(item) {
       //notificao de esterilizacao
      var resultado = confirm(` Deseja avançar para a situação: ${item.get_next_situacao} `)
      if (resultado) {
        if (item.get_next_situacao_url) {
          this.loadingDepositos = true;
          this.$http.patch(item.get_next_situacao_url).then((response) => {
              //console.log(response)
              this.getDepositos();
            })
          /*
          this.$http.patch(item.get_next_situacao).then((teste) => {
            console.log(teste)
            this.getDepositos(situacao);
          })
          */
            .catch((error) => {
              console.error(error);
            })
            .finally(() => {
              this.loadingDepositos = false;
            });
        }
      }
    },
    atualizarDeposito(deposito) {
     // console.log(deposito)
      //return false
       //notificao de esterilizacao
      var resultado = confirm(` Deseja avançar etapa dos itens de depósitos?  `)
      if (resultado) {
          this.loadingDepositos = true;
          this.$http.patch(deposito.get_rud_url).then((response) => {
              //console.log(response)
              this.getDepositos();
            })
          /*
          this.$http.patch(item.get_next_situacao).then((teste) => {
            console.log(teste)
            this.getDepositos(situacao);
          })
          */
            .catch((error) => {
              console.error(error);
            })
            .finally(() => {
              this.loadingDepositos = false;
            });
      }
    },
    updateDeposito(deposito) {
      this.atualizarDeposito(deposito)
    },
    initialize() {
      this.getDepositos();
    },
    getDepositos(filtro = "") {
      var url = "{{getDepositos}}?filtro=" + filtro
      this.loadingDepositos = true;
      this.$http.get(url).then((response) => {
          this.depositos = response.data;
         //console.log(response.data)
        }).catch((error) => {
          alert(error);
          this.depositos = [];
        }).finally(() => {
          this.loadingDepositos = false;
        });

    },
    getColor(situacao) {
      switch (situacao) {
        case this.computedAEsterilizar:
          return "error";
          break;
        case this.computedEsterilizando:
          return "warning";
          break;
        case this.computedEsterilizado:
          return "info";
          break;
        case this.computedEntregue:
          return "success";
          break;
        default:
          return "success";
      }
    },

    gerar_etiqueta(item) {
      var etiqueta = "";

      for (var i = 1; i <= item.quantidade; i++) {
        etiqueta += `<samp>
            
          <div style="margin:3px;padding:10px;width:350px;border-radius:5px;border-style: solid; background: #fff"; center center>
            <div>
              <span id="barcode ${item.get_depositante_username}"></span>
              <span style="float:right; font-size:25px; font-weight:bold">[  ]</span>
            </div>
            <div style="font-size:40px; font-weight:bold">${(
              "0000000" + item.id
            ).slice(-7)}</div>
            <div>Depositante: ${item.get_depositante_username}</div>
            <div>${item.get_depositante_nome}</div>

            <div>${item.tipo_box.tipo_volume}: ${item.tipo_box.nome_volume} - Vol: <b>${i} / ${
          item.quantidade
        }</b> </div>
            <div style="width: 250px;white-space: nowrap;overflow: hidden;text-overflow: ellipsis;">
              Obs: ${item.observacoes || ''}
            </div>
            <hr>
            <div>
              <span>Usuário: ${item.criado_por}</span>
              <span style="float:right">${item.get_criado_em}</span>
            </div>
          </div>
        </samp>
        `;
      }
      return etiqueta;
    },
    imprimir(itens = []) {
      var corpo_etiqueta = "";

      for (var i = 0; i < itens.length; i++) {
        corpo_etiqueta += this.gerar_etiqueta(itens[i]);
      }
      var w = window.open();
      w.document.write(corpo_etiqueta);

      w.print();
    },
  },
});
</script>