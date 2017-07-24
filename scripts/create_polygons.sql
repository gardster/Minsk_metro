drop table if exists minsk_polygons;

create table minsk_polygons as (
    with segments as (
        select
            (ST_Dump(
                ST_Transform(
                    ST_VoronoiPolygons(
                        ST_Collect(
                            ST_SetSRID(
                                ST_MakePoint(
                                    ST_X(
                                        ST_Transform(point, 3857)
                                    )::bigint,
                                    ST_Y(
                                        ST_Transform(point, 3857)
                                    )::bigint
                                ),
                                3857
                            )
                        )
                ),
                3857
                )
            )).geom as geom
        from
            minsk_points
        )
    select
        ST_Transform(geom, 4326) as geom,
        greatest(ceil(duration/300.0), 1) as duration
    from
        segments
        left join minsk_points on ST_Intersects(geom, point)
);

drop table if exists minsk_areas;

create table minsk_areas as (
    select
        duration,
        ST_Union(geom) as geom
    from
        minsk_polygons
    group by 1
);

update minsk_areas set geom = (select ST_Union(geom) from minsk_areas where duration >3) where duration = 4;
delete from minsk_areas where duration>4;
