WITH vendas_brutas AS (
    SELECT * FROM raw.raw_vendas
)

SELECT
    id_venda,
    id_cliente,
    id_produto,
    id_loja,
    data_venda,
    quantidade,
    valor_unitario,
    (quantidade * valor_unitario) AS valor_total
FROM vendas_brutas