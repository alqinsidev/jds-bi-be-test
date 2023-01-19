
# BANK DATA STUNTING JABAR

An API Service that Provide Stunting Case data in Jawa Barat
## Authors

- [@alqinsidev](https://www.github.com/alqinsidev)


## Appendix

Technology used on this service :

- REST API Service Powered by [FastAPI](https://fastapi.tiangolo.com/)
- PostgreSQL Database with [SQLAlchemy](https://sqlalchemy.org) ORM
- Service are hosted and deployed as Docker Container on AWS EC2 Free Tier
- CI/CD by Github Actions
- Unit test by [pytest](https://pytest.org)

## API Reference

Here are some usefull End Point on the service, every data provided can be visualized as Barchart or Piechart.

#### Get all items

```http
    GET /stunting
```

Retrieve all of data about stunting case in jawa barat

#### Get data by Kabupaten / Kota

```http
    GET /stunting/kabupaten-kota/${id}
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | **Required**. kode kabupaten/kota |

this end point retrieve all stunting case summary for specific kabupaten/kota in jawa barat

#### Get yearly case data

 ```http
    GET /stunting/jumlah-kasus/
```

Retrieve yearly total case of stunting in jawa barat


#### Get Kabupaten / Kota with yearly higest number

 ```http
    GET /stunting/kasus-tertinggi/
```

Retrieve Kabupaten / Kota with higest stunting number per year
## Demo

Service entry point can be found [here](http://18.142.250.106:2701/).

Service documentation can be found [here](http://18.142.250.106:2701/docs). Please use this word as Bearer token for every protected Route.

`token-jabar-juara`

## To Do

This application is prematurly deployed, so many things need to upgrade on this application. For instance :

- Better documentation
- Environment management
- Project Folder Structure
- Implementing JWT Bearer / OAuth rather than dummy token
