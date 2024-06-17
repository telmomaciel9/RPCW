## Descarregar o dataset sobre a História de Portugal e sobre ele responder às seguintres questões:

### Quantos triplos existem na Ontologia?

```
Select * where{
    ?s ?p ?o .
}
```

### Que classes estão definidas?

```
Select * where{
    ?s rdf:type owl:Class .
}
```

### Que propriedades tem a classe "Rei"?

``` 
Select ?prop where{
    ?s rdf:type historia:Rei .
    ?s ?prop ?o .
}
```

### Quantos reis aparecem na ontologia?

````
Select * where{
    ?s rdf:type historia:Rei .
}
````


### Calcula uma tabela com o seu nome, data de nascimento e cognome.

````
Select ?s ?nome ?cognomes ?nascimento where{
    ?s rdf:type historia:Rei ;
       historia:nome ?nome ;
       historia:cognomes ?cognomes ;
       historia:nascimento ?nascimento .
}
````



### Acrescenta à tabela anterior a dinastia em que cada rei reinou.

````
Select ?s ?nome ?cognomes ?nascimento ?dinastia ?dnome where{
    ?s rdf:type historia:Rei ;
       historia:nome ?nome ;
       historia:cognomes ?cognomes ;
       historia:nascimento ?nascimento .
    ?s historia:temReinado ?reinado .
    ?reinado historia:dinastia ?dinastia .
    ?dinastia historia:nome ?dnome
}
````



### Qual a distribuição de reis pelas 4 dinastias?




### Lista os decobrimentos (sua descrição) por ordem cronológica.
### Lista as várias conquistas, nome e data, juntamento com o nome que reinava no momento.
### Calcula uma tabela com o nome, data de nascimento e número de mandatos de todos os presidentes portugueses.
### Quantos mandatos teve o presidente Sidónio Pais? Em que datas iniciaram e terminaram esses mandatos?
### Quais os nomes dos partidos políticos presentes na ontologia?
### Qual a distribuição dos militantes por cada partido político?
### Qual o partido com maior número de presidentes militantes? 