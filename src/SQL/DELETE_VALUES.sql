USE dw_estacoes_green;

-- Desativar o modo de atualização segura temporariamente
SET SQL_SAFE_UPDATES = 0;

-- Deletar registros das tabelas
DELETE FROM fato_green;
DELETE FROM dim_estacao;
DELETE FROM dim_vento;
DELETE FROM tempo;

-- Reativar o modo de atualização segura
SET SQL_SAFE_UPDATES = 1;

select * from fato_green, dim_estacao, dim_vento, dim_tempo;