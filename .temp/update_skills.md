seguinte quero organizar a estrutura dos agentes

agent/rules/uso_python_obrigatorio.md 

workflows/apelidar_tabela.md (incluir uma coluna de apelido na planilha )
workflows/criar_bd_apelido.md (banco de dados com apelido e regras para apelidar )
workflows/criar_script_apelidos.md (codigo python apelidar descricao e unidade )
workflows/loop_desconhecidos.md (caso não seja encontrado apelido criar e apelidas conforme skills )

agent/skills/excel_to_csv/skill.md (converter o excel para csv) 
agent/skills/excel_to_csv/scripts/excel_to_csv.py, converter o excel to csv usar try para mais de um metodo python puro, numpy, pandas)
agent/skills/excel_to_csv/scripts/inicio_tabela.py, identificar o inicio da tabela quando tem (id, descricao, unid, qtd,unit parcial,) )
agent/skills/excel_to_csv/scripts/colunas_relevantes.py (id, descricao, unid, qtd,unit, parcial )
agent/skills/excel_to_csv/scripts/colunas_obrigatoria.py (id, descricao, qtd,unid )
agent/skills/excel_to_csv/exemplos/ ( exemplos de titulos de tabela) 
agent/skills/excel_to_csv/resource/ ( sinonimos de nome de tabela)

agent/skills/normalizar_descricao/skill.md (tudo minusculo, remover preposição, remover acentos...) 
agent/skills/normalizar_descricao/scripts/normalizar_tabela.py
agent/skills/normalizar_descricao/scripts/manter_unicos_tabela.py ( eliminar nomes descrição repetidos, remover espaços duplos)
agent/skills/normalizar_descricao/scripts/normalizar_numeros_tabela.py ( normalizar numeros decimais)
agent/skills/normalizar_descricao/exemplos/ ( exemplos de tabela) 
agent/skills/normalizar_descricao/resource/ ( melhores praticas do etl)

agent/skills/normalizar_unidade/skill.md (tudo minusculo, remover preposição, remover acentos, remover espaço...) 
agent/skills/normalizar_unidade/scripts/converter_unidade.py (m² > m2, metro > m, m3> m3, normalizar nomes)
agent/skills/normalizar_unidade/exemplos/ (lista_unidades) 
agent/skills/normalizar_unidade/resource/ (unidades dos sistema internacional SI)
agent/skills/normalizar_unidade/resource/ (unidades dos sistema imperial)

agent/skills/criar_apelido/skill.md (criar apelido baseado na descrição e unidade e juntar nome_unidade de uma planilha) 
agent/skills/criar_apelido/scripts/criar_apelido.py (escavacao_m3, escavacao_mec_solo_m3, escavacao_mec_vala_solo_m3)
agent/skills/criar_apelido/scripts/manter_unicos_tabela.py ( eliminar nomes descrição repetidos)
agent/skills/criar_apelido/exemplos/ ( tabela de exemplo apelidos, tem não tem ) 
agent/skills/criar_apelido/resource/ ( escavacao_m3, escavacao_mec_solo_m3, escavacao_mec_vala_solo_m3)
agent/skills/criar_apelido/resource/ ( literatura de taxonomia)
agent/skills/criar_apelido/resource/ ( formato de como apelidar na obra nas construção)
agent/skills/criar_apelido/resource/ ( servico_material_metodo_unidade, formato)


