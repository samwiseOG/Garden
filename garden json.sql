-- Table: public.Garden Json

-- DROP TABLE IF EXISTS public."Garden Json";

CREATE TABLE IF NOT EXISTS public."Garden Json"
(
    "recordId" integer NOT NULL DEFAULT nextval('"Garden Json_recordId_seq"'::regclass),
    "startTimestamp" time with time zone NOT NULL,
    "sensorId" character varying(12) COLLATE pg_catalog."default" NOT NULL,
    "unit" character varying(20) COLLATE pg_catalog."default",
    "valuesJsonb" jsonb,
    "valuesJson" json,
    CONSTRAINT "Garden Json_pkey" PRIMARY KEY ("recordId")
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."Garden Json"
    OWNER to postgres;