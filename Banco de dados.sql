CREATE TABLE Alunos (
    Id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    Nome VARCHAR(100)
);

CREATE TABLE Notas (
    Id SERIAL PRIMARY KEY,
    IdAluno UUID REFERENCES Alunos(Id),
    Nota DECIMAL(5, 2)
);