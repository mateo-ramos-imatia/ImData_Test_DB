CREATE OR REPLACE VIEW v_mobi_operations_with_masters AS (
select co.*, 
cmot.constant_id as operation_type_constant_id,
ctot.name as operation_type_name,
ifnull(sum(cou.price * cou.units), 0) AS SUB_PRECIO,
ifnull(sum(cou.cost * cou.units), 0) AS SUB_COSTE
from cor_operations co 
left join cor_tra_operation_types ctot on co.id_operation_type = ctot.id_operation_type and ctot.id_language = 1
left join cor_mst_operation_types cmot on co.id_operation_type = cmot.id_operation_type and cmot.id_tenant = ctot.id_tenant
left join cor_outsourcings cou on co.id_operation = cou.id_operation and co.id_tenant = cou.id_tenant 
group by co.id_operation 
);

CREATE OR REPLACE VIEW v_mobi_operations_labours_prices AS(
select 
co.id_operation,
ifnull(sum(case when ifnull(cl.discount, 0) > 0 then cl.units * (cl.price_per_hour * cl.minutes / 60) - cl.price_per_hour * cl.minutes / 60 * cl.discount / 100 else cl.units * (cl.price_per_hour * cl.minutes / 60) end), 0) AS LAB_PRECIO_NETO,
ifnull(sum(cl.units * (cl.price_per_hour * cl.minutes / 60)), 0) AS LAB_PRECIO_BRUTO,
ifnull(sum(cl.units * (cl.cost_per_hour * cl.minutes / 60)), 0) AS LAB_COSTE
from cor_operations co 
left join cor_labours cl on co.id_operation = cl.id_operation and co.id_tenant = cl.id_tenant 
group by co.id_operation
);

CREATE OR REPLACE VIEW v_mobi_operations_materials_prices AS (
select co.id_operation,
ifnull(sum(cm.price * cm.units), 0) AS MAT_PRECIO,
ifnull(sum(case when cm.discount > 0 then cm.price * cm.units - cm.price * (cm.discount / 100) else cm.price * cm.units end), 0) AS MAT_PRECIO_NETO,
ifnull(sum(cm.cost * cm.units), 0) AS MAT_COSTE
from cor_operations co
left join cor_materials cm on cm.id_operation = co.id_operation and cm.id_tenant = co.id_tenant
group by co.id_operation
);

CREATE OR REPLACE VIEW v_mobi_operations_severals_prices AS (
select co.id_operation,
ifnull(sum(cs.price * cs.units), 0) AS SEV_PRECIO,
ifnull(sum(cs.cost * cs.units), 0) AS SEV_COSTE
from cor_operations co
left join cor_severals cs on cs.id_operation = co.id_operation and cs.id_tenant = co.id_tenant
group by co.id_operation
);

CREATE OR REPLACE VIEW v_mobi_operations_other_concepts_prices AS (
select co.id_operation,
ifnull(sum(coc.price * coc.units), 0) AS OTR_PRECIO,
ifnull(sum(coc.cost * coc.units), 0) AS OTR_COSTE
from cor_operations co
left join cor_other_concepts coc on co.id_operation = coc.id_operation and co.id_tenant = coc.id_tenant
group by co.id_operation
);


-- Pequeña modificacion en v_mobi_workshop_entries
-- Se agrega el campo cro.id_reparation_order y se quita el tenant 7 del filtrado.

CREATE OR REPLACE VIEW v_mobi_workshop_entries AS (
	select
		cmt.id_tenant as id_tenant,	
		cmt.name as Tenant,
		cc2.id_company as id_company,
		cc2.name as Compañia,
		cc.id_center as id_Center,
		cc.name as Centro,
		cro.id_reparation_order,
		concat('OR-',cro.serie,'/',cro.year) as OR_formato,
		cc3.vin as vin,
		co.id_operation,
		co.name,
		co.code, 
		co.operation_type_name as nombre_tipo_operacion,
		co.operation_type_constant_id as tipo_operacion_cteId,
		co.cost as coste,
		co.price as precio,
		lp.LAB_PRECIO_NETO,
		lp.LAB_PRECIO_BRUTO,
		lp.LAB_COSTE,
		mp.MAT_PRECIO,
		mp.MAT_PRECIO_NETO,
		mp.MAT_COSTE,
		sp.SEV_PRECIO,
		sp.SEV_COSTE,
		co.SUB_PRECIO, 
		co.SUB_COSTE,
		cocp.OTR_PRECIO,
		cocp.OTR_COSTE
	from cor_reparation_orders cro 
	left join cor_centers cc on cro.id_center = cc.id_center 
	left join cor_mst_tenants cmt on cro.id_tenant = cmt.id_tenant
	left join cor_companies cc2 on cc.id_company = cc2.id_company
	left join cor_chassis cc3 on cro.id_equipment = cc3.id_vehicle
	left join v_mobi_operations_with_masters co on co.id_reparation_order = cro.id_reparation_order
	left join v_mobi_operations_labours_prices lp on co.id_operation = lp.id_operation
	left join v_mobi_operations_materials_prices mp on co.id_operation = mp.id_operation
	left join v_mobi_operations_severals_prices sp on co.id_operation = sp.id_operation
	left join v_mobi_operations_other_concepts_prices cocp on co.id_operation = cocp.id_operation
	where 
	cc3.vin is not null and cmt.name not like '%OBSOLETO' and cc2.name not like '%OBSOLETO' and cc.id_tenant not in (1,3,6) 
	order by id_tenant
);

-- ********************version con CTEs******************************************
WITH v_mobi_operations_with_masters AS (
select 
	co.*, 
	cmot.constant_id as operation_type_constant_id,
	ctot.name as operation_type_name,
	ifnull(sum(cou.price * cou.units), 0) AS SUB_PRECIO,
	ifnull(sum(cou.cost * cou.units), 0) AS SUB_COSTE,
	'EXTERNO' as tipo_cargo
from cor_operations co 
	left join cor_tra_operation_types ctot 
		on co.id_operation_type = ctot.id_operation_type 
		and ctot.id_language = 1
	left join cor_mst_operation_types cmot 
		on co.id_operation_type = cmot.id_operation_type 
		and cmot.id_tenant = ctot.id_tenant
	left join cor_outsourcings cou 
		on co.id_operation = cou.id_operation 
		and co.id_tenant = cou.id_tenant 
group by co.id_operation 
),
v_mobi_operations_labours_prices AS(
select 
	co.id_operation,
	ifnull(sum(case when ifnull(cl.discount, 0) > 0 then cl.units * (cl.price_per_hour * cl.minutes / 60) - cl.price_per_hour * cl.minutes / 60 * cl.discount / 100 else cl.units * (cl.price_per_hour * cl.minutes / 60) end), 0) AS LAB_PRECIO_NETO,
	ifnull(sum(cl.units * (cl.price_per_hour * cl.minutes / 60)), 0) AS LAB_PRECIO_BRUTO,
	ifnull(sum(cl.units * (cl.cost_per_hour * cl.minutes / 60)), 0) AS LAB_COSTE,
	'MANO DE OBRA' as tipo_cargo
from cor_operations co 
	left join cor_labours cl 
		on co.id_operation = cl.id_operation 
		and co.id_tenant = cl.id_tenant 
group by co.id_operation
),
v_mobi_operations_materials_prices AS (
select 
	co.id_operation,
	ifnull(sum(cm.price * cm.units), 0) AS MAT_PRECIO,
	ifnull(sum(case when cm.discount > 0 then cm.price * cm.units - cm.price * (cm.discount / 100) else cm.price * cm.units end), 0) AS MAT_PRECIO_NETO,
	ifnull(sum(cm.cost * cm.units), 0) AS MAT_COSTE,
	'ECOTASAS' as tipo_cargo
from cor_operations co
	left join cor_materials cm
		on cm.id_operation = co.id_operation
		and cm.id_tenant = co.id_tenant
group by co.id_operation
),
v_mobi_operations_severals_prices AS (
select 
	co.id_operation,
	ifnull(sum(cs.price * cs.units), 0) AS SEV_PRECIO,
	ifnull(sum(cs.cost * cs.units), 0) AS SEV_COSTE,
	'VARIOS' as tipo_cargo
from cor_operations co
	left join cor_severals cs 
		on cs.id_operation = co.id_operation
		and cs.id_tenant = co.id_tenant
group by co.id_operation
),
v_mobi_operations_other_concepts_prices AS (
select 
	co.id_operation,
	ifnull(sum(coc.price * coc.units), 0) AS OTR_PRECIO,
	ifnull(sum(coc.cost * coc.units), 0) AS OTR_COSTE
from cor_operations co
	left join cor_other_concepts coc
		on co.id_operation = coc.id_operation
		and co.id_tenant = coc.id_tenant
group by co.id_operation
)
select
	cmt.id_tenant as id_tenant,	
	cmt.name as Tenant,
	cc2.id_company as id_company,
	cc2.name as Compañia,
	cc.id_center as id_Center,
	cc.name as Centro,
	cro.id_reparation_order,
	concat('OR-',cro.serie,'/',cro.year) as OR_formato,
	cc3.vin as vin,
	co.id_operation,
	co.name,
	co.code, 
	co.operation_type_name as nombre_tipo_operacion,
	co.operation_type_constant_id as tipo_operacion_cteId,
	co.cost as coste,
	co.price as precio,
	lp.LAB_PRECIO_NETO,
	lp.LAB_PRECIO_BRUTO,
	lp.LAB_COSTE,
	mp.MAT_PRECIO,
	mp.MAT_PRECIO_NETO,
	mp.MAT_COSTE,
	sp.SEV_PRECIO,
	sp.SEV_COSTE,
	co.SUB_PRECIO, 
	co.SUB_COSTE,
	cocp.OTR_PRECIO,
	cocp.OTR_COSTE,
	co.tipo_cargo as tipo_cargo_externo,
	lp.tipo_cargo as tipo_cargo_mano_obra,
	mp.tipo_cargo as tipo_cargo_materiales,
	sp.tipo_cargo as tipo_cargo_varios
from cor_reparation_orders cro 
	left join cor_centers cc 
		on cro.id_center = cc.id_center 
	left join cor_mst_tenants cmt 
		on cro.id_tenant = cmt.id_tenant
	left join cor_companies cc2 
		on cc.id_company = cc2.id_company
	left join cor_chassis cc3 
		on cro.id_equipment = cc3.id_vehicle
	left join v_mobi_operations_with_masters co 
		on co.id_reparation_order = cro.id_reparation_order
	left join v_mobi_operations_labours_prices lp 
		on co.id_operation = lp.id_operation
	left join v_mobi_operations_materials_prices mp 
		on co.id_operation = mp.id_operation
	left join v_mobi_operations_severals_prices sp 
		on co.id_operation = sp.id_operation
	left join v_mobi_operations_other_concepts_prices cocp 
		on co.id_operation = cocp.id_operation
where 
cc3.vin is not null and cmt.name not like '%OBSOLETO' and cc2.name not like '%OBSOLETO' and cc.id_tenant not in (1,3,6) 
order by id_tenant


-- ********************version sin vistas intermedias******************************************

select
	cmt.id_tenant as id_tenant,	
	cmt.name as Tenant,
	cc2.id_company as id_company,
	cc2.name as Compañia,
	cc.id_center as id_Center,
	cc.name as Centro,
	cro.id_reparation_order,
	concat('OR-',cro.serie,'/',cro.year) as OR_formato,
	cc3.vin as vin,
	co.id_operation,
	co.name,
	co.code, 
	co.operation_type_name as nombre_tipo_operacion,
	co.operation_type_constant_id as tipo_operacion_cteId,
	co.coste,
	co.precio,
	lp.LAB_PRECIO_NETO,
	lp.LAB_PRECIO_BRUTO,
	lp.LAB_COSTE,
	mp.MAT_PRECIO,
	mp.MAT_PRECIO_NETO,
	mp.MAT_COSTE,
	sp.SEV_PRECIO,
	sp.SEV_COSTE,
	co.SUB_PRECIO, 
	co.SUB_COSTE,
	cocp.OTR_PRECIO,
	cocp.OTR_COSTE
from cor_reparation_orders cro 
	left join cor_centers cc on cro.id_center = cc.id_center 
	left join cor_mst_tenants cmt on cro.id_tenant = cmt.id_tenant
	left join cor_companies cc2 on cc.id_company = cc2.id_company
	left join cor_chassis cc3 on cro.id_equipment = cc3.id_vehicle
	left join (
		select
			co.id_operation,
			co.id_reparation_order,
			co.name,
			co.code,
			co.cost as coste,
			co.price as precio,
			cmot.constant_id as operation_type_constant_id,
			ctot.name as operation_type_name,
			ifnull(sum(cou.price * cou.units), 0) AS SUB_PRECIO,
			ifnull(sum(cou.cost * cou.units), 0) AS SUB_COSTE
		from cor_operations co 
			left join cor_tra_operation_types ctot 
				on co.id_operation_type = ctot.id_operation_type 
				and ctot.id_language = 1
			left join cor_mst_operation_types cmot 
				on co.id_operation_type = cmot.id_operation_type 
				and cmot.id_tenant = ctot.id_tenant
			left join cor_outsourcings cou 
				on co.id_operation = cou.id_operation 
				and co.id_tenant = cou.id_tenant 
		group by 
			co.id_operation,
			co.id_reparation_order,
			co.name,
			co.code,
			co.cost,
			co.price,
			cmot.constant_id,
			ctot.name
	) as co on co.id_reparation_order = cro.id_reparation_order
	left join (
		select 
			co.id_operation,
			ifnull(
				sum(
					case when ifnull(cl.discount, 0) > 0 
						then cl.units * (cl.price_per_hour * cl.minutes / 60) - cl.price_per_hour * cl.minutes / 60 * cl.discount / 100 
						else cl.units * (cl.price_per_hour * cl.minutes / 60) 
						end
				)
			, 0) AS LAB_PRECIO_NETO,
			ifnull(sum(cl.units * (cl.price_per_hour * cl.minutes / 60)), 0) AS LAB_PRECIO_BRUTO,
			ifnull(sum(cl.units * (cl.cost_per_hour * cl.minutes / 60)), 0) AS LAB_COSTE
		from cor_operations co 
			left join cor_labours cl 
				on co.id_operation = cl.id_operation 
				and co.id_tenant = cl.id_tenant 
		group by co.id_operation
	) as lp on co.id_operation = lp.id_operation
	left join (
		select 
			co.id_operation,
			ifnull(sum(cm.price * cm.units), 0) AS MAT_PRECIO,
			ifnull(
				sum(
					case when cm.discount > 0 
						then cm.price * cm.units - cm.price * (cm.discount / 100) 
						else cm.price * cm.units 
					end
				), 0
			) AS MAT_PRECIO_NETO,
			ifnull(sum(cm.cost * cm.units), 0) AS MAT_COSTE
		from cor_operations co
			left join cor_materials cm 
				on cm.id_operation = co.id_operation 
				and cm.id_tenant = co.id_tenant
		group by co.id_operation
	) as mp on co.id_operation = mp.id_operation
	left join (
		select 
			co.id_operation,
			ifnull(sum(cs.price * cs.units), 0) AS SEV_PRECIO,
			ifnull(sum(cs.cost * cs.units), 0) AS SEV_COSTE
		from cor_operations co
			left join cor_severals cs 
			on cs.id_operation = co.id_operation 
			and cs.id_tenant = co.id_tenant
		group by co.id_operation
	) sp on co.id_operation = sp.id_operation
	left join (
		select 
			co.id_operation,
			ifnull(sum(coc.price * coc.units), 0) AS OTR_PRECIO,
			ifnull(sum(coc.cost * coc.units), 0) AS OTR_COSTE
		from cor_operations co
			left join cor_other_concepts coc 
			on co.id_operation = coc.id_operation 
			and co.id_tenant = coc.id_tenant
		group by co.id_operation
	) cocp on co.id_operation = cocp.id_operation
where 
	cc.id_importer = 5 
	and cc3.vin is not null 
	and cmt.name not like '%OBSOLETO' 
	and cc2.name not like '%OBSOLETO' 
	and cc.id_tenant not in (1,3,6) 
order by 
	id_tenant;

-- ********************************************************************************************
-- Vista con todas las Ors facturadas, ya sea cliente como garantias como participaciones

create or replace view v_mobi_invoiced_ors as(
	select 
		cro.id_reparation_order,
		cro.id_tenant
	FROM cor_reparation_orders cro 
	left join cor_invoices_reparation_orders ciro 
		on ciro.id_reparation_order = cro.id_reparation_order 
	left join cor_invoice_reparation_orders ciro2 
		on ciro.id_invoice_reparation_order = ciro2.id_invoice_reparation_order 
	left join cor_invoice_series cis 
		on ciro2.id_invoice_series = cis.id_invoice_series 
		and ciro2.id_tenant = cis.id_tenant 
	left join cor_mst_invoice_series_types cmist 
		on cis.id_invoice_series_type = cmist.id_invoice_series_type 
		and cis.id_tenant = cmist.id_tenant
	left join cor_centers cc 
		on cro.id_tenant = cc.id_tenant
	where 
		ciro2.id_invoice_reparation_order_rectified_by is null 
		and cmist.constant_id = 1 
		and cc.id_importer = 5 
		and cc.name not like '%OBSOLETO' 
		and cro.id_tenant not in (1,3,6)
union
	select
		co.id_reparation_order,
		co.id_tenant
	from cor_free_invoice_lines cfil
	left join cor_bulletins cb
		on cfil.id_bulletin = cb.id
		and cfil.id_tenant = cb.id_tenant
	left join cor_operations_bulletin cob
		on cb.id  = cob.id_bulletin
		and cob.id_tenant = cb.id_tenant
	left join cor_operations co
		on cob.id_operation = co.id_operation
	left join cor_free_invoices_free_invoice_lines cfifil
		on cfil.id_free_invoice_line = cfifil.id_free_invoice_line
	left join cor_free_invoices cfi
		on cfifil.id_free_invoice = cfi.id_free_invoice
		and cfil.id_tenant = cfi.id_tenant
	left join cor_invoice_series cis
		on cfi.id_invoice_series = cis.id_invoice_series
		and cfi.id_tenant = cis.id_tenant 
	left join cor_mst_invoice_series_types cmist
		on cis.id_invoice_series_type = cmist.id_invoice_series_type
		and cis.id_tenant = cmist.id_tenant 
	left join cor_centers cc
		on co.id_tenant = cc.id_tenant
	where 
		cfil.id_bulletin is not NULL
		and cmist.constant_id = 1
		and cc.id_importer = 5
		and cc.name not like '%OBSOLETO'
		and co.id_tenant not in (1,3,6)
union
	select 
		co2.id_reparation_order,
		co2.id_tenant
	from cor_free_invoice_lines cfil 
	left join cor_bulletins cb
		on cfil.id_bulletin = cb.id
		and cfil.id_tenant = cb.id_tenant 
	left join cor_participations_bulletin cpb
		on cb.id = cpb.id_bulletin
		and cb.id_tenant = cpb.id_tenant 
	left join cor_participations cp
		on cpb.id_participation = cp.id
		and cpb.id_tenant = cp.id_tenant
	left join cor_operations co2
		on cp.id_operation = co2.id_operation
	left join cor_free_invoices_free_invoice_lines cfifil
		on cfil.id_free_invoice_line = cfifil.id_free_invoice_line 
	left join cor_free_invoices cfi
		on cfifil.id_free_invoice = cfi.id_free_invoice
		and cfil.id_tenant = cfi.id_tenant 
	left join cor_invoice_series cis
		on cfi.id_invoice_series = cis.id_invoice_series
		and cfi.id_tenant = cis.id_tenant 
	left join cor_mst_invoice_series_types cmist
		on cis.id_invoice_series_type = cmist.id_invoice_series_type
		and cis.id_tenant = cmist.id_tenant 
	left join cor_centers cc
		on co2.id_tenant = cc.id_tenant
	where 
		cfil.id_bulletin is not null
		and cmist.constant_id = 1
		and cc.id_importer = 5
		and cc.name not like '%OBSOLETO'
		and co2.id_tenant not in (1,3,6)
);
	
-- Vista que filtra las entradas de taller con aquellas que estan facturadas.
create or replace view v_bussines_amount as (
	select vmwe.* 
	from v_mobi_workshop_entries vmwe 
	left join v_mobi_invoiced_ors vmio
		on vmwe.id_reparation_order = vmio.id_reparation_order
		and vmwe.id_tenant = vmio.id_tenant
);
	