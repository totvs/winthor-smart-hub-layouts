
# Winthor Smart Hub Layouts

A fim de melhorar o controle e o versionamento dos layouts criados e alterados, bem como facilitar a implantação do Winthor Smart Hub, foram criados layouts com padrões pré-definidos. O Winthor Smart Hub atua como um intermediário entre duas APIs distintas, facilitando a comunicação entre elas. Ele é essencial em integrações de sistemas heterogêneos, onde as APIs têm diferentes formatos de dados, autenticação, endpoints e outros aspectos. para realiza a comunicação entre apis. Existem dois layouts principais: de transformação e comunicação, eles podem, através deste repositório, ser facilmente ajustados e versionados de acordo com as necessidades específicas de integração de cada projeto. Isso proporciona uma maior flexibilidade e agilidade no desenvolvimento e na manutenção das integrações.
 
## Funcionalidades
- Versionamento de layouts de transformação e Comunicação;
- Roteamento de servicos de busca e envio entre as empresas APIs;
- Manipulação de variáveis fixas e dinâmicas;
- Layouts de Transformação: Responsáveis por converter os dados de um formato para outro, adequando-os aos requisitos da API de destino.
- Layouts de Comunicação: Definem a estrutura e os parâmetros necessários para realizar a comunicação entre as APIs, incluindo autenticação, endpoints e manipulação de erros.

#### Api para instalação do layout

```http
  POST /winthor/integracao/fulfillment/v1/layout/
```

| Parâmetro   | Tipo       | Descrição                           |
| :---------- | :--------- | :---------------------------------- |
| `projetoNome` | `string` | **Obrigatório**. Nome layout a ser instalado |
| `versao` | `string` | **Obrigatório**. Versão do layout a ser instalado |
| `caminhoLayout` | `string` | **Não Obrigatório**. Caminho para a pasta de layouts (apenas em modo de desenvolvimento) |
| `ambiente` | `string` | **Não Obrigatório**. Ambiente de Produção ou Homologação (padrão Homologação)|


## Alteração ou Criação de Layouts

Clone o repositório winthor-smart-hub-layouts:

```bash
  git clone https://github.com/totvs/winthor-smart-hub-layouts.git
```
Crie um novo Branch (mesmo padrão do Azure e Bitbucket "feature/DWSHWTNG-123-criarRotaVendasTeste-develop");

```bash
https://github.com/totvs/winthor-smart-hub-layouts/branches  
```
Faça o checkout

```bash
git checkout feature/DWSHWTNG-123-criarRotaVendasTeste-develop
```

Abra a pasta winthor-smart-hub-layouts e escolha o layout:

```bash
 cd C:\fontesGit\winthor-smart-hub-layouts\pdvsync

```    
Para cada rota criada, adicione um novo arquivo no formato ".json" dentro da pasta "rotas":
```bash
 cd C:\fontesGit\winthor-smart-hub-layouts\pdvsync\rotas\PDVSYNC - BUSCAR VENDAS TESTE.json
```    
Considere o conteúdo abaixo para criar o arquivo de rotas:
```bash
{
    "tabela": {
        "nome": "PCINTEGRACAOROTASERVICO",
        "campos": [
            {
                "nome": "ID",
                "valor": "PDVSYNC - BUSCAR VENDAS TESTE"
            },
            {
                "nome": "IDEMPRESAAPI",
                "valor": "PDVSYNC"
            },
            {
                "nome": "SERVICO",
                "valor": "PDVSYNC - BUSCAR VENDAS TESTE"
            },
            {
                "nome": "LAYOUTCOMUNICACAO",
                "valor": _INSIRA_O_LAYOUT_EXTRAIDO_DO_POSTMAN,
            {
                "nome": "LAYOUTTRANSFORMACAO",
                "valor": _INSIRA_O_LAYOUT_EXTRAIDO_DO_JOLT,
            {
                "nome": "ATIVO",
                "valor": "S"
            } 
        ]       
    }
}