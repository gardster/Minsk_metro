delete from minsk_points where ctid in (
    select
        ctid
    from
    (
        select
            ctid,
            row_number() over (partition by point order by duration) as rnum
        from
            minsk_points
    ) t
    where
        t.rnum > 1
);
