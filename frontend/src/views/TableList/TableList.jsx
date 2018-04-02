import React from "react";
import { Grid } from "material-ui";

import { RegularCard, Table, ItemGrid } from "components";

function TableList({ ...props }) {
  return (
    <Grid container>
      <ItemGrid xs={12} sm={12} md={12}>
        <RegularCard
          cardTitle="Padrón de cabilderos"
          cardSubtitle="Listado de servidores públicos vinculados con empresas en el sector hidrocarburos"
          content={
            <Table
              tableHeaderColor="primary"
              tableHead={["Nombre", "Cargo", "Estado", "Salario"]}
              tableData={[
                ["Juan Perez", "Diputado", "Puebla", "$36,738"],
                ["Manuel Gomez", "Senador", "Veracruz", "$23,789"],
                ["Pablo Jimenez", "Contralor", "Chiapas", "$56,142"],
                ["José Mendez", "Finanzas", "Oaxaca", "$38,735"],
                ["Juana García", "Persidente Municipal", "Yucatan", "$63,542"],
                ["Pedro Martínez", "Diputado", "Guerrero", "$78,615"]
              ]}
            />
          }
        />
      </ItemGrid>
      <ItemGrid xs={12} sm={12} md={12}>
        <RegularCard
          plainCard
          cardTitle="Table on Plain Background"
          cardSubtitle="Here is a subtitle for this table"
          content={
            <Table
              tableHeaderColor="primary"
              tableHead={["ID", "Nombre", "Country", "City", "Salary"]}
              tableData={[
                ["1", "Dakota Rice", "$36,738", "Niger", "Oud-Turnhout"],
                ["2", "Minerva Hooper", "$23,789", "Curaçao", "Sinaai-Waas"],
                ["3", "Sage Rodriguez", "$56,142", "Netherlands", "Baileux"],
                [
                  "4",
                  "Philip Chaney",
                  "$38,735",
                  "Korea, South",
                  "Overland Park"
                ],
                [
                  "5",
                  "Doris Greene",
                  "$63,542",
                  "Malawi",
                  "Feldkirchen in Kärnten"
                ],
                ["6", "Mason Porter", "$78,615", "Chile", "Gloucester"]
              ]}
            />
          }
        />
      </ItemGrid>
    </Grid>
  );
}

export default TableList;
