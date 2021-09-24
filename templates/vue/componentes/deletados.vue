 <Botão para avançar status -->
                        {% if request.user.is_staff %}
                       
                        <v-btn 
                          small
                          depressed 
                          label
                        :disabled="dItem.situacao == computedEntregue"
                          v-if="dItem.situacao != computedEntregue && dItem.situacao != computedEsterilizado"
                          :loading="loadingDepositos"
                          dark
                          :color="getColor(dItem.situacao)"
                          ><@click="updateSituacao(dItem)"
                          <v-progress-circular
                          small
                          :color="getColor(dItem.situacao)" 
                          size="0"         
                          ></v-progress-circular>                      
                        <v-icon>mdi-chevron-double-right</v-icon>
                        </v-btn>    
                         validar user
                        <loginuser :loading="loading" ref="loginuser" :username="item.usuario.username" :show-username="false"
                          v-if="dItem.situacao == computedEsterilizado" label='Entregar' :block="false"
                          @validate-password="validarEntrega($event,item.usuario, dItem)"></loginuser> 
                          <br>
                        {% else %}
                    
                        <v-chip
                          label
                          dark
                          small
                          :color="getColor(dItem.situacao)"
                          :title="[[dItem.situacao]]"
                        >
                          <v-icon>mdi-circle</v-icon> &nbsp; [[dItem.situacao]]
                        </v-chip>-->
                        {% endif %}