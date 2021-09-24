<template id="depositarcaixa">
	<v-dialog max-width="900px" :fullscreen="$vuetify.breakpoint.smAndDown" scrollable v-model="dialog">
		<template v-slot:activator="{ on, attrs }">
			{% if request.user.is_staff %}
			<v-btn 
				:block="$vuetify.breakpoint.xsOnly" :loading="loadingDepositos || loadingCaixas"
				elevation="0" :color="$vuetify.theme.themes.light.accent" dark class="mx-1 mb-1" v-bind="attrs" v-on="on">
				Novo Depósito
			</v-btn>
			{% endif %}
		</template>
		<v-card>
			<v-card-title>
				Incluir depósitos
				<v-spacer></v-spacer>
				<v-btn @click="dialog = false" icon> <v-icon> mdi-close </v-icon></v-btn>
			</v-card-title>
			<v-card-text>
				<v-row dense>
					<v-col sm="5" md="5" lg="5" cols="12">
						<div v-if="loadingCaixas">
							<v-progress-circular size="70" indeterminate color="success"></v-progress-circular>
						</div>
						<div v-else>
							<v-row v-for="(item, index) in caixasLista" :key="'caixa_'+index" dense>
								<v-col  cols="12">
									<div>
										<v-card outlined tile width="100%" class="text-center mr-2" style="text-align-last: left;">
											<span class="group pa-2">
											<v-btn class="ma-2" color="#215f5e" fab
												@click="() => (item.quantidade > 0 ? item.quantidade-- : 0)" dark small elevation="0">
											<v-icon small>mdi-minus</v-icon>
											</v-btn>
											<span class="title ">[[item.quantidade]]</span>
											<v-btn class="ma-2" color="#215f5e" fab @click="() => item.quantidade++" dark small elevation="0">
											<v-icon small>mdi-plus</v-icon>
											</v-btn>
											</span>
										<strong><span v-text="item.nome_volume"></span></strong>
										</v-card>
									</div>
								</v-col>
							</v-row>
						</div>
					</v-col>
					<v-col sm="5" md="5" lg="5" cols="12">
						<v-card class="pa-2" outlined tile>
							Seu depósitos: 
							<div v-if="loadingDepositos">
								<v-progress-circular size="70" indeterminate color="info"></v-progress-circular>

							</div>
							<div v-else>
								<samp>
									<div class="depositos">
										<div v-for="deposito in selectedDepositos" :key="'deposito_caixa_' + deposito.id" id="deposito">
											<div>
												[[deposito.tipo_volume]] - [[deposito.nome_volume]] -
												[[deposito.quantidade]]
											</div>
											<div>
												<v-text-field v-model="deposito.observacoes" 
													:label="`Observações para ${deposito.nome_volume}`"></v-text-field>
											</div>
										</div>
									</div>
								</samp>
							</div>
						</v-card>
					</v-col>
					<v-col sm="2" md="2" lg="2" cols="12">
						<loginuser v-if="selectedDepositos.length > 0" 
							@validate-password="validacaoPassword($event)"></loginuser>
						
						<v-btn block class="my-1" color="#215f5e"  dark @click="this.cleanItemAdd" small>
							<v-icon v-if="$vuetify.breakpoint.mdAndUp" dark left > mdi-delete </v-icon>
							Limpar
						</v-btn>
						<v-btn block class="my-1" color="#215f5e"  dark small @click="dialog = false">
							<v-icon v-if="$vuetify.breakpoint.mdAndUp" dark left> mdi-cancel </v-icon>
							Cancelar
						</v-btn>
					</v-col>
				</v-row>
			</v-card-text>
		</v-card>
	</v-dialog>
</template>

{% url 'box:api_caixas' as getCaixas %}
{% url 'box:api_deposito' as postDeposito %}

{% include 'vue/componentes/loginuser.vue' %}

<script>
Vue.component("depositarcaixa", {
  template: "#depositarcaixa",
  delimiters: ["[[", "]]"],
  data: () => ({
	caixas: [],
	itemAdd: { id: null, quantidade: 0 },
	selectedDepositos: [],
	caixasLista: [],
	capturar: [],
	dialog: false,
	loadingCaixas:false,
	loadingDepositos: false
  }),
  computed: {
	color() {
	  if (this.itemAdd < 2) return "indigo";
	},
	computedEsterilizar(){
		return 'ESTERILIZAR';
	},
	computedEsterilizando(){
		return 'ESTERILIZANDO';
	},
	computedEsterilizado(){
		return 'ESTERILIZADO';
	},
	computedEntregue(){
		return 'ENTREGUE';
	},
  },
  methods: {
	
	validacaoPassword(usuario_id) {
	  // //console.log('validação no componente PAI', usuario_id)
	  ////console.log('enviar o id do usuario RA:', usuario_id)
	  // //console.log('enviar os depositos:', this.selectedDepositos)
	  if (usuario_id) {
		var postObject = {
		  usuario: usuario_id,
		  depositos: this.selectedDepositos.map((obj) => {
			return {
			  tipo_box: obj.id,
			  quantidade: obj.quantidade,
			  situacao: this.computedEsterilizar,
			  observacoes: obj.observacoes
			};
		  }),
		};
		this.postDepositoItem(postObject);
	  }
	},
	decrement() {
	  this.item.quantidade--;
	},
	incrrement() {
	  this.quantidade++;
	},
	cleanItemAdd() {
	  this.getCaixas();
	},
	buildObject() {
	  this.selectedDepositos = this.caixasLista.filter(
		(item) => item.quantidade > 0
	  );
	//  //console.log(this.selectedDepositos);
	},
	getCaixas(){
		this.loadingCaixas = true
		this.$http.get("{{getCaixas}}").then((response) => {
			this.caixas = response.body.sort((a, b) => b.nome_volume.length - a.nome_volume.length);

			this.selectCaixas(this.caixas);
			}).catch((error) => {
			console.error(error);
			}).finally(()=>{
				this.loadingCaixas = false
			});
	},
	postDepositoItem(postObject) {
	  this.loadingDepositos = true
	  this.$http.post("{{postDeposito}}", postObject).then((response) => {
		  alert('Depósito realizado com sucesso')
		  this.dialog = false
		  this.$emit('deposito-added',true)
		  //console.log(response);
		}).catch((error) => {
		  //console.log(error);
		  try {
			alert(error.data[0]);
		  } catch {
			alert(error.data);
		  }
		}).finally(()=>{
			this.loadingDepositos = false
		});
	},
	selectCaixas(array) {
	  this.caixasLista = array.map((itemCaixa) => {
		itemCaixa = { ...itemCaixa, quantidade: 0 };
		return itemCaixa;
	  });
	},
  },
  mounted() {
	  this.getCaixas();
  },
  watch: {
	itemAdd: {
	  handler(value) {
		//console.log(value);
	  },
	  deep: true,
	},
	dialog(value) {
	  if (value) {
		this.cleanItemAdd();
		//console.log("Limpando sempre fechar aba de esterelizar", value);
	  }
	},
	caixasLista: {
	  handler(value) {
		//console.log(value);
		this.buildObject();
	  },
	  deep: true,
	},
  },
});
</script>

<style scoped>
	.depositos{
		border-radius:5px !important;
		background:#eee;
		color: black;
		font-size:12px;
		padding:5px;
	}
</style>