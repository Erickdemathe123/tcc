from datetime import datetime
from app.extensions import db

TIPOS_OCORRENCIA = ['Praga', 'Doença']

NIVEIS_SEVERIDADE = ['Leve', 'Moderada', 'Grave']

PRAGAS_DOENCAS_COMUNS = [
    'Sigatoka-negra',
    'Sigatoka-amarela',
    'Mal-do-Panamá',
    'Moko',
    'Broca-do-rizoma',
    'Trips',
    'Pulgão',
    'Ácaro',
    'Nematoides',
    'Antracnose',
    'Outros',
]

RECOMENDACOES = {
    'Sigatoka-negra': {
        'tipo': 'Doença',
        'agente': 'Fungo Mycosphaerella fijiensis',
        'descricao': 'Doença fúngica que causa manchas necróticas nas folhas, reduzindo a área fotossintética e a qualidade dos frutos.',
        'Leve': [
            'Remover e destruir folhas com mais de 50% da área afetada.',
            'Aplicar fungicida protetor à base de mancozebe ou clorotalonil.',
            'Monitorar semanalmente a evolução das manchas.',
            'Evitar molhamento excessivo das folhas na irrigação.',
        ],
        'Moderada': [
            'Aplicar fungicida sistêmico (propiconazol, tebuconazol ou triadimenol) em alternância com protetores.',
            'Realizar desfolha completa das folhas muito afetadas.',
            'Melhorar drenagem e espaçamento entre plantas para reduzir umidade.',
            'Reavaliar em 15 dias e repetir aplicação se necessário.',
        ],
        'Grave': [
            'Implementar programa intensivo de fungicidas sistêmicos em rotação (trifloxistrobina, azoxistrobina, propiconazol) a cada 10–14 dias.',
            'Eliminar plantas com mais de 75% das folhas comprometidas.',
            'Destruir todo o material vegetal doente (queima ou enterrio).',
            'Consultar engenheiro agrônomo para laudo e prescrição oficial.',
            'Considerar replantio com variedades mais resistentes.',
        ],
        'prevencao': [
            'Usar mudas sadias e certificadas.',
            'Realizar desfolha preventiva periodicamente.',
            'Manter boa drenagem e evitar excesso de umidade.',
            'Monitorar com escala de Stover modificada.',
        ],
    },
    'Sigatoka-amarela': {
        'tipo': 'Doença',
        'agente': 'Fungo Mycosphaerella musicola',
        'descricao': 'Doença fúngica semelhante à Sigatoka-negra, porém menos agressiva. Causa estrias amareladas que evoluem para manchas marrons.',
        'Leve': [
            'Remover folhas com sintomas iniciais (estrias amarelas).',
            'Aplicar fungicida protetor (mancozebe, propinebe).',
            'Monitorar a evolução a cada 10 dias.',
        ],
        'Moderada': [
            'Aplicar fungicida sistêmico (propiconazol ou carbendazim).',
            'Intensificar desfolha e retirada de restos culturais.',
            'Verificar e corrigir a drenagem do solo.',
        ],
        'Grave': [
            'Alternar fungicidas sistêmicos e protetores em calendário semanal.',
            'Eliminar plantas muito debilitadas.',
            'Consultar agrônomo para avaliação da área e prescrição.',
        ],
        'prevencao': [
            'Monitoramento regular das folhas mais jovens.',
            'Desfolha preventiva periódica.',
            'Evitar irrigação por aspersão sobre as folhas.',
        ],
    },
    'Mal-do-Panamá': {
        'tipo': 'Doença',
        'agente': 'Fungo Fusarium oxysporum f. sp. cubense',
        'descricao': 'Doença vascular sem cura que pode devastar plantações inteiras. O fungo persiste no solo por décadas. Declaração obrigatória ao MAPA.',
        'Leve': [
            'Isolar imediatamente as plantas com sintomas (amarelecimento e murcha de folhas mais velhas).',
            'Desinfectar ferramentas com hipoclorito de sódio 10% entre cada planta.',
            'Não movimentar solo, mudas ou material vegetal da área afetada.',
            'Notificar a Secretaria de Agricultura ou MAPA.',
        ],
        'Moderada': [
            'Erradicar todas as plantas doentes e adjacentes (raio de 2 m), incluindo rizomas.',
            'Destruir o material por queima no local.',
            'Realizar calagem intensiva do solo (pH > 7).',
            'Suspender o plantio de bananeiras na área por no mínimo 2 anos.',
            'Substituir por variedades resistentes à Raça 4 (ex.: Grand Naine, FHIA-18).',
        ],
        'Grave': [
            'Notificar imediatamente o MAPA — a doença é de notificação compulsória.',
            'Interditar e quarentenar a área afetada.',
            'Erradicar total do bananal com queima e enterrio dos restos.',
            'Não replantio de bananeiras por pelo menos 5 anos.',
            'Biofumigação do solo com plantas do gênero Brassica antes do replantio.',
        ],
        'prevencao': [
            'Usar exclusivamente mudas certificadas e livres do patógeno.',
            'Desinfetar calçados e equipamentos ao entrar no talhão.',
            'Preferir variedades resistentes em áreas de risco.',
            'Nunca introduzir material vegetal de origem desconhecida.',
        ],
    },
    'Moko': {
        'tipo': 'Doença',
        'agente': 'Bactéria Ralstonia solanacearum (Raça 2)',
        'descricao': 'Doença bacteriana vascular, altamente destrutiva e de notificação obrigatória. Transmitida por ferramentas, insetos, água e solo.',
        'Leve': [
            'Isolar imediatamente as plantas suspeitas com fita ou cerca.',
            'Desinfetar TODAS as ferramentas antes e depois de cada uso (álcool 70% ou hipoclorito 10%).',
            'Notificar a Defesa Agropecuária estadual.',
            'Não realizar nenhuma poda ou corte nas plantas suspeitas.',
        ],
        'Moderada': [
            'Erradicar as plantas doentes sem cortar o cacho (para não dispersar a bactéria).',
            'Aplicar herbicida sistêmico no pseudocaule para matar a planta in situ antes de removê-la.',
            'Destruir por queima dentro da área.',
            'Interditar o talhão para trânsito de pessoas e animais.',
            'Comunicar o MAPA imediatamente.',
        ],
        'Grave': [
            'AÇÃO IMEDIATA: notificar o MAPA — doença de notificação compulsória.',
            'Interditar e sinalizar toda a área com quarentena.',
            'Erradicar total do bananal com uso de herbicida sistêmico + queima.',
            'Quarentena mínima de 6 meses a 1 ano antes de qualquer novo plantio.',
            'Controlar insetos visitantes de flores (vetores) com inseticidas.',
        ],
        'prevencao': [
            'Desinfecção rigorosa de ferramentas entre plantas.',
            'Não transitar entre talhões sem lavar botas e equipamentos.',
            'Usar mudas certificadas e livres de Ralstonia.',
            'Controle de insetos polinizadores que podem transmitir a bactéria.',
        ],
    },
    'Broca-do-rizoma': {
        'tipo': 'Praga',
        'agente': 'Besouro Cosmopolites sordidus',
        'descricao': 'Praga que ataca o rizoma e pseudocaule, causando galerias que enfraquecem a planta, reduzem a produção e facilitam entrada de patógenos.',
        'Leve': [
            'Instalar iscas com pedaços de pseudocaule (30 cm) ao redor das plantas, cobertos com folhas.',
            'Coletar e destruir os adultos capturados nas iscas diariamente.',
            'Monitorar com armadilhas de feromônio (Cosmolure).',
            'Sanitizar a área removendo restos de colheita e pseudocaules velhos.',
        ],
        'Moderada': [
            'Aplicar nematicida/inseticida sistêmico no solo (carbofurano ou terbufós — seguir legislação vigente).',
            'Intensificar iscas e armadilhas de feromônio.',
            'Retirar e destruir pseudocaules muito infestados.',
            'Usar controle biológico com fungo Beauveria bassiana.',
        ],
        'Grave': [
            'Aplicar inseticida sistêmico no rizoma e solo ao redor da touceira.',
            'Destruir plantas com mais de 40% do rizoma comprometido.',
            'Implementar rotina de iscas + feromônio + controle biológico integrado.',
            'Consultar agrônomo para plano de manejo integrado de pragas (MIP).',
        ],
        'prevencao': [
            'Usar mudas tratadas e inspecionadas (rizoma limpo).',
            'Manter limpeza do talhão (sem restos de pseudocaule).',
            'Monitoramento mensal com armadilhas de feromônio.',
            'Nunca plantar rizomas de origem duvidosa.',
        ],
    },
    'Trips': {
        'tipo': 'Praga',
        'agente': 'Frankliniella parvula e outras espécies',
        'descricao': 'Insetos minúsculos que atacam flores e frutos jovens, causando cicatrizes e manchas na casca que depreciam a qualidade comercial.',
        'Leve': [
            'Empacotar os cachos logo após a emissão da pencas com sacos plásticos microperfurados.',
            'Preservar inimigos naturais (ácaros predadores, percevejos Orius).',
            'Monitorar contagem de trips por flor semanalmente.',
        ],
        'Moderada': [
            'Aplicar inseticida específico (espinosade, abamectina) na flor e pencas jovens.',
            'Remover frutos danificados para evitar foco de multiplicação.',
            'Embalar cachos imediatamente após emergência.',
            'Reaplicar em 7–10 dias se necessário.',
        ],
        'Grave': [
            'Rotacionar inseticidas (espinosade + imidacloprido ou tiametoxam) para evitar resistência.',
            'Empacotar 100% dos cachos assim que emergir a flor.',
            'Consultar agrônomo para diagnóstico e receituário agronômico.',
        ],
        'prevencao': [
            'Embalar cachos preventivamente após abertura da última penca.',
            'Monitoramento semanal nos meses mais quentes e secos.',
            'Conservar a vegetação ao redor para manter predadores naturais.',
        ],
    },
    'Pulgão': {
        'tipo': 'Praga',
        'agente': 'Pentalonia nigronervosa (vetor do vírus Bunchy top)',
        'descricao': 'Além do dano direto por sucção de seiva, o pulgão é o principal vetor do vírus Banana Bunchy Top Virus (BBTV), que causa o "topo-em-leque".',
        'Leve': [
            'Preservar predadores naturais: joaninhas (Cycloneda), crisopídeos, parasitoides.',
            'Eliminar formigas que cultivam os pulgões (aplicar barreira de cola no pseudocaule).',
            'Aplicar óleo mineral ou óleo de nim como repelente.',
            'Inspecionar a base das folhas e o pseudocaule regularmente.',
        ],
        'Moderada': [
            'Aplicar inseticida sistêmico (imidacloprido ou tiametoxam) no solo ou foliar.',
            'Eliminar formigas com iscas específicas (gel de hidramethylnon).',
            'Verificar se há sintomas de vírus Bunchy top nas plantas próximas.',
        ],
        'Grave': [
            'Aplicar inseticida sistêmico e de contato em combinação.',
            'Erradicar plantas com sintomas de BBTV (folhas estreitas, encurvadas, com "leque").',
            'Notificar presença de BBTV ao órgão de defesa vegetal — é quarentenária no Brasil.',
            'Consultar agrônomo imediatamente.',
        ],
        'prevencao': [
            'Inspecionar mudas antes do plantio para presença de pulgões.',
            'Controlar formigas no talhão.',
            'Monitorar semanalmente a base das folhas mais novas.',
        ],
    },
    'Ácaro': {
        'tipo': 'Praga',
        'agente': 'Tetranychus urticae, Aceria guerreronis (ácaro-da-quiasma)',
        'descricao': 'Ácaros que atacam folhas e frutos. O ácaro-da-quiasma causa a "mancha-da-quiasma" nos frutos, depreciando a qualidade exportação.',
        'Leve': [
            'Aumentar a umidade relativa do ar (irrigação localizada).',
            'Aplicar enxofre molhável ou óleo de nim como acaricida alternativo.',
            'Preservar ácaros predadores (Neoseiulus californicus, Phytoseiulus persimilis).',
        ],
        'Moderada': [
            'Aplicar acaricida específico (abamectina, propargite ou bifenazate).',
            'Cobrir os cachos para proteger os frutos do ácaro-da-quiasma.',
            'Reavaliar em 10 dias e repetir se a população não cair.',
        ],
        'Grave': [
            'Alternar acaricidas com diferentes mecanismos de ação para evitar resistência.',
            'Aplicar sobre frutos e folhas (face abaxial) com cobertura total.',
            'Consultar agrônomo — em casos de resistência pode ser necessária receita agronômica.',
        ],
        'prevencao': [
            'Monitoramento semanal das folhas (face inferior) e dos frutos.',
            'Manter adequada irrigação e umidade no talhão.',
            'Conservar inimigos naturais evitando inseticidas desnecessários.',
        ],
    },
    'Nematoides': {
        'tipo': 'Praga',
        'agente': 'Radopholus similis, Meloidogyne spp., Pratylenchus spp.',
        'descricao': 'Parasitas microscópicos das raízes que causam necrose, redução da ancoragem e tombamento das plantas, além de queda de produção.',
        'Leve': [
            'Usar mudas certificadas e livres de nematoides (mudas micropropagadas).',
            'Incorporar matéria orgânica para estimular fungos nematofágicos.',
            'Biofumigação com Crotalaria juncea ou nabo-forrageiro como adubo verde.',
        ],
        'Moderada': [
            'Aplicar nematicida biológico (Purpureocillium lilacinum, Bacillus firmus).',
            'Incorporar torta de mamona ou nim no solo.',
            'Renovar raízes: cortar o pseudocaule e deixar rebrotar a planta.',
            'Adquirir mudas apenas de viveiros certificados para replantio.',
        ],
        'Grave': [
            'Aplicar nematicida químico (oxamil ou fluensulfone — com receituário agronômico).',
            'Destruir plantas muito afetadas (raízes necrosadas > 50%).',
            'Erradicar e realizar pousio por 6–12 meses com incorporação de matéria orgânica.',
            'Replantio apenas com mudas micropropagadas e limpas.',
        ],
        'prevencao': [
            'Nunca usar mudas de campo (chifrinho) sem inspeção e tratamento.',
            'Rotação de culturas na área antes do replantio.',
            'Manter solo com boa estrutura e matéria orgânica.',
            'Evitar estresse hídrico que agrava os danos das raízes.',
        ],
    },
    'Antracnose': {
        'tipo': 'Doença',
        'agente': 'Fungo Colletotrichum musae',
        'descricao': 'Principal doença pós-colheita da banana. Causa manchas escuras na casca durante o amadurecimento, podendo atingir a polpa.',
        'Leve': [
            'Colher no ponto correto (75–80% de maturação, coloração verde).',
            'Aplicar fungicida pós-colheita (tiabendazol ou imazalil) nos frutos antes do armazenamento.',
            'Manter cadeia de frio adequada (13–14 °C) durante transporte e armazenamento.',
        ],
        'Moderada': [
            'Realizar tratamento hidrotérmico dos frutos (51–53 °C por 5 minutos).',
            'Aplicar cera protetora com fungicida incorporado.',
            'Melhorar as condições de armazenamento e reduzir danos mecânicos no manuseio.',
        ],
        'Grave': [
            'Descartar frutos muito afetados (não comercializar).',
            'Aplicar fungicida + cera em 100% dos cachos da safra restante.',
            'Revisar todo o processo de colheita, embalagem e transporte para reduzir ferimentos.',
            'Consultar agrônomo para prescrição de programa de controle pós-colheita.',
        ],
        'prevencao': [
            'Evitar ferimentos nos frutos durante colheita e transporte.',
            'Manter higiene dos equipamentos de colheita e galpão.',
            'Não misturar frutos de lotes diferentes no armazenamento.',
            'Controlar Sigatoka (as lesões nas folhas são fonte de inóculo).',
        ],
    },
    'Outros': {
        'tipo': 'Indefinido',
        'agente': 'Agente não identificado',
        'descricao': 'Ocorrência de agente ainda não identificado. Diagnóstico laboratorial é recomendado antes de qualquer intervenção.',
        'Leve': [
            'Coletar amostras das partes afetadas (folhas, raízes, frutos) para diagnóstico.',
            'Fotografar os sintomas e registrar as condições do talhão.',
            'Isolar preventivamente as plantas afetadas.',
            'Consultar engenheiro agrônomo para identificação.',
        ],
        'Moderada': [
            'Enviar amostras para laboratório de fitopatologia ou entomologia.',
            'Aplicar medidas de contenção (isolamento, higiene de ferramentas) enquanto aguarda diagnóstico.',
            'Não aplicar agroquímicos sem diagnóstico confirmado.',
        ],
        'Grave': [
            'Contactar imediatamente o serviço de defesa agropecuária estadual ou o MAPA.',
            'Interditar preventivamente o acesso ao talhão.',
            'Paralisar qualquer movimentação de plantas ou solo da área.',
            'Aguardar diagnóstico oficial antes de qualquer intervenção de erradicação.',
        ],
        'prevencao': [
            'Manter monitoramento regular do talhão.',
            'Registrar qualquer sintoma novo assim que aparecer.',
            'Ter contato de engenheiro agrônomo de referência.',
        ],
    },
}


class Ocorrencia(db.Model):
    __tablename__ = 'ocorrencias'

    id = db.Column(db.Integer, primary_key=True)
    talhao_id = db.Column(db.Integer, db.ForeignKey('talhoes.id'), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    data_ocorrencia = db.Column(db.Date, nullable=False)
    severidade = db.Column(db.String(20), nullable=False)
    area_afetada_ha = db.Column(db.Float)
    tratamento_aplicado = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Ocorrencia {self.nome} - {self.data_ocorrencia}>'
