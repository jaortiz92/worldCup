-- Inserción de los 48 equipos (Mundial 2026 - Custom Draw)
INSERT INTO teams (id, code_iso, name, flag_url, groups) VALUES

-- Grupo A
(1, 'MEX', 'México', 'https://flagcdn.com/mx.svg', 'A'),
(2, 'ZAF', 'Sudáfrica', 'https://flagcdn.com/za.svg', 'A'),
(3, 'KOR', 'Corea del Sur', 'https://flagcdn.com/kr.svg', 'A'),
(4, 'CZE', 'República Checa', 'https://flagcdn.com/cz.svg', 'A'),

-- Grupo B
(5, 'CAN', 'Canadá', 'https://flagcdn.com/ca.svg', 'B'),
(6, 'BIH', 'Bosnia y Herzegovina', 'https://flagcdn.com/ba.svg', 'B'),
(7, 'QAT', 'Qatar', 'https://flagcdn.com/qa.svg', 'B'),
(8, 'SUI', 'Suiza', 'https://flagcdn.com/ch.svg', 'B'),

-- Grupo C
(9, 'BRA', 'Brasil', 'https://flagcdn.com/br.svg', 'C'),
(10, 'MAR', 'Marruecos', 'https://flagcdn.com/ma.svg', 'C'),
(11, 'HAI', 'Haití', 'https://flagcdn.com/ht.svg', 'C'),
(12, 'SCO', 'Escocia', 'https://flagcdn.com/gb-sct.svg', 'C'),

-- Grupo D
(13, 'USA', 'Estados Unidos', 'https://flagcdn.com/us.svg', 'D'),
(14, 'PAR', 'Paraguay', 'https://flagcdn.com/py.svg', 'D'),
(15, 'AUS', 'Australia', 'https://flagcdn.com/au.svg', 'D'),
(16, 'TUR', 'Turquía', 'https://flagcdn.com/tr.svg', 'D'),

-- Grupo E
(17, 'GER', 'Alemania', 'https://flagcdn.com/de.svg', 'E'),
(18, 'CUW', 'Curazao', 'https://flagcdn.com/cw.svg', 'E'),
(19, 'CIV', 'Costa de Marfil', 'https://flagcdn.com/ci.svg', 'E'),
(20, 'ECU', 'Ecuador', 'https://flagcdn.com/ec.svg', 'E'),

-- Grupo F
(21, 'NED', 'Países Bajos', 'https://flagcdn.com/nl.svg', 'F'),
(22, 'JPN', 'Japón', 'https://flagcdn.com/jp.svg', 'F'),
(23, 'SWE', 'Suecia', 'https://flagcdn.com/se.svg', 'F'),
(24, 'TUN', 'Túnez', 'https://flagcdn.com/tn.svg', 'F'),

-- Grupo G
(25, 'BEL', 'Bélgica', 'https://flagcdn.com/be.svg', 'G'),
(26, 'EGY', 'Egipto', 'https://flagcdn.com/eg.svg', 'G'),
(27, 'IRN', 'Irán', 'https://flagcdn.com/ir.svg', 'G'),
(28, 'NZL', 'Nueva Zelanda', 'https://flagcdn.com/nz.svg', 'G'),

-- Grupo H
(29, 'ESP', 'España', 'https://flagcdn.com/es.svg', 'H'),
(30, 'CPV', 'Cabo Verde', 'https://flagcdn.com/cv.svg', 'H'),
(31, 'KSA', 'Arabia Saudita', 'https://flagcdn.com/sa.svg', 'H'),
(32, 'URU', 'Uruguay', 'https://flagcdn.com/uy.svg', 'H'),

-- Grupo I
(33, 'FRA', 'Francia', 'https://flagcdn.com/fr.svg', 'I'),
(34, 'SEN', 'Senegal', 'https://flagcdn.com/sn.svg', 'I'),
(35, 'IRQ', 'Irak', 'https://flagcdn.com/iq.svg', 'I'),
(36, 'NOR', 'Noruega', 'https://flagcdn.com/no.svg', 'I'),

-- Grupo J
(37, 'ARG', 'Argentina', 'https://flagcdn.com/ar.svg', 'J'),
(38, 'ALG', 'Argelia', 'https://flagcdn.com/dz.svg', 'J'),
(39, 'AUT', 'Austria', 'https://flagcdn.com/at.svg', 'J'),
(40, 'JOR', 'Jordania', 'https://flagcdn.com/jo.svg', 'J'),

-- Grupo K
(41, 'POR', 'Portugal', 'https://flagcdn.com/pt.svg', 'K'),
(42, 'COD', 'República Democrática del Congo', 'https://flagcdn.com/cd.svg', 'K'),
(43, 'UZB', 'Uzbekistán', 'https://flagcdn.com/uz.svg', 'K'),
(44, 'COL', 'Colombia', 'https://flagcdn.com/co.svg', 'K'),

-- Grupo L
(45, 'ENG', 'Inglaterra', 'https://flagcdn.com/gb-eng.svg', 'L'),
(46, 'CRO', 'Croacia', 'https://flagcdn.com/hr.svg', 'L'),
(47, 'GHA', 'Ghana', 'https://flagcdn.com/gh.svg', 'L'),
(48, 'PAN', 'Panamá', 'https://flagcdn.com/pa.svg', 'L')

-- Manejo de conflictos (Idempotencia)
ON CONFLICT (id) DO UPDATE SET
    code_iso = EXCLUDED.code_iso,
    name = EXCLUDED.name,
    flag_url = EXCLUDED.flag_url,
    groups = EXCLUDED.groups;