drop table if exists minsk_points;

create table minsk_points (point geometry, duration float);

create index on minsk_points using gist(point);
