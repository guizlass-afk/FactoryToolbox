# Factory Toolbox

Portal das ferramentas de projeto e fabricação: View & Convert, PipeSaver, BestSection, EZNesting e LaymanCAD 2D.

- Cartões grandes com descrições e links diretos para os cinco projetos.
- Página responsiva, com navegação por teclado e preferência por movimento reduzido.
- Doze idiomas, bandeiras locais, preferência salva e leitura RTL em árabe.
- Ao abrir uma ferramenta, o portal grava o idioma na chave já usada por ela no mesmo domínio GitHub Pages. Se o armazenamento estiver bloqueado, os links continuam funcionando.
- HTML, CSS e JavaScript sem dependências externas, etapa de build ou serviços de tradução.

## Workspace canônico

`\\192.168.15.73\Users\guizl_rede\compartilhamento\Projetos\Factory Toolbox`

Trabalhar diretamente nesta pasta compartilhada. Este repositório é independente dos repositórios das ferramentas.

## Desenvolvimento

Execute `python -m http.server 8080` nesta pasta e abra `http://localhost:8080`.

Os links e cartões estão em `index.html`; traduções em `translations.js`; comportamento do seletor em `app.js`.

## Publicação

GitHub Pages publica a raiz da branch `main` em https://guizlass-afk.github.io/FactoryToolbox/.

## Validação

`python tests/test_portal.py` requer Python, Playwright e Chrome. Verifica links, idiomas, persistência, teclado, RTL e apresentação em tamanhos de tela diferentes.


## Aparência

O botão de sol/lua ao lado do idioma alterna os temas claro e escuro. A preferência fica salva em `factorytoolbox-theme`, compartilhada entre as ferramentas no mesmo domínio. Sem escolha salva, o tema acompanha a preferência do sistema. Alterar o tema mantém o projeto e os resultados atuais. A impressão e os arquivos exportados preservam as cores do desenho.

## Licenciamento do código próprio

O código original desta versão tem todos os direitos reservados, conforme `LICENSE`. Esta versão do código próprio não é distribuída sob a licença MIT. As licenças e os avisos de componentes de terceiros são preservados.

Validação integrada de temas: `python tests/test_themes.py`, com os cinco repositórios nas pastas irmãs do compartilhamento. Inclui preferência do sistema, persistência, sincronização entre abas, teclado, rótulos traduzidos, impressão, modelo 3D, folha A4 e regressões dos otimizadores.
