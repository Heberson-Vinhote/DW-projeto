-- 1. Receita total por categoria de produto
SELECT
    p.categoria,
    SUM(v.valor_total) as receita_total
FROM fato_vendas v
JOIN dim_produto p ON v.id_produto = p.id_produto
GROUP BY p.categoria
ORDER BY receita_total DESC;

-- 2. Top 5 clientes em volume de compras
SELECT
    c.nome,
    c.estado,
    SUM(v.valor_total) as total_compras,
    COUNT(v.id_venda) as qtd_pedidos
FROM fato_vendas v
JOIN dim_cliente c ON v.id_cliente = c.id_cliente
GROUP BY c.nome, c.estado
ORDER BY total_compras DESC
LIMIT 5;

-- 3. Vendas por mês/ano (Sazonalidade)
SELECT
    t.ano,
    t.mes,
    SUM(v.valor_total) as receita_mensal
FROM fato_vendas v
JOIN dim_tempo t ON v.data_venda = t.data
GROUP BY t.ano, t.mes
ORDER BY t.ano, t.mes;

-- 4. Desempenho de vendas por Loja
SELECT
    l.nome_loja,
    l.cidade,
    SUM(v.valor_total) as receita_total
FROM fato_vendas v
JOIN dim_loja l ON v.id_loja = l.id_loja
GROUP BY l.nome_loja, l.cidade
ORDER BY receita_total DESC;
