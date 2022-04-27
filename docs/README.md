# Comroom Backend Documents

## DB Schema (AWS DynamoDB)

### Table: `School`

```json
{
  "name": "충북/삼양초등학교", //pk
  "code": "hashed-6",
  "reg_date": "2022-04-30",
  "comrooms": [
    {
        "name": "컴1실",
        "desc": "본관 3층",
        "is_deleted": false
    },
    {
        "name": "컴2실",
        "desc": "후관 2층",
        "is_deleted": false
    }
  ],
  "admin": {
    "name": "이은섭",
    "id": "ssamko",
    "email": "ssamko@kakao.com",
    "password": "hashed",
    "is_active": false,
    "token": "token key"
  }
}
```

### Table: `Timetable`

```json
{
  "school_comroom": "충북/삼양초등학교/0", //pk
  "datetime": "2022-04-30/09:00-09:40", //sk
  "grade": "6학년",
  "class": "4반",
  "teacher": "이은섭",
  "password": 1234
}
```

### Table: `FixedTimetable`

```json
{
  "school_comroom": "충북/삼양초등학교/0", // pk
  "weekday": 3, // 목요일
  "title": "수업",
  "hour": "09:00-09:40",
  "start_date": "2022-04-30",
  "end_date": "2023-04-30" // sk
}
```

### Table: `Notice`

```json
{
  "title": "3.0 업데이트", // pk
  "contents": "업데이트 완료",
  "isShow": true
}
```

GSI
| index name   | primary_key  |
| ------------ | ------------ |
| isShow-Index | isShow(bool) |

## Query

### Get monthly timetable

```bash
aws dynamodb query \
    --table-name Timetable \
    --key-condition-expression "school_comroom = :name and begins_with(datetime, :dt)" \
    --expression-attribute-values  file://values.json
```

> values.json
>
>```json
>{
>    ":name":{"S":"충북/삼양초등학교/0"},
>    ":dt":{"S":"2022-04"}
>}
>```

### Get fixed_monthly

```bash
aws dynamodb query \
    --table-name FixedTimetable \
    --key-condition-expression "school_comroom = :name and end_date >= :dt" \
    --filter-expresion "#st <= :dt" \
    --expression-attribute-names '{"#st": "start_date"}'
    --expression-attribute-values  file://values.json
```

> values.json
>
> ```json
> {
>    ":name":{"S":"충북/삼양초등학교/0"},
>    ":dt":{"S":"2022-04-01"}
>}
> ```
