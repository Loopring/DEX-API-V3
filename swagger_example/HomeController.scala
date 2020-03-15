package controllers

import io.swagger.annotations._
import javax.inject._
import play.api.libs.json.{Format, Json}
import play.api.mvc._
import play.api._
import scala.concurrent.Future

@ApiModel(description = "下单请求对象")
case class SubmitOrderRequest(
    @ApiModelProperty(value = "交易所ID", example = "1", required = true)
    exchangeId: Int,
    @ApiModelProperty(value = "订单ID", example = "1", required = true)
    orderId: Int,
    @ApiModelProperty(value = "账户ID", example = "1", required = true)
    accountId: Int,
    @ApiModelProperty(value = "selling token id in exchange", example = "0",
        required = true)
    tokenSId: Int,
    @ApiModelProperty(value = "buying token id in exchange", example = "2",
        required = true)
    tokenBId: Int,
    @ApiModelProperty(value = "selling amount of token, decimal string in WEI",
        example = "1000000000000000000", required = true)
    amountS: String,
    @ApiModelProperty(value = "buying amount of token, decimal string in WEI",
        example = "1000000000000000000", required = true)
    amountB: String,
    @ApiModelProperty(value = "all or none", dataType = "boolean", example =
          "false")
    allOrNone: Option[Boolean] = None,
    @ApiModelProperty(value = "buy", dataType = "boolean", example = "true")
    buy: Option[Boolean] = None,
    @ApiModelProperty(value =
          "beginning period of this order, timestamp in second", example =
          "1567053142", required = true)
    validSince: Long,
    @ApiModelProperty(value = "ending period of this order, timestamp in second",
        example = "1567053142", required = true)
    validUntil: Long,
    @ApiModelProperty(value =
          "max accepted fee of this order, selling amount times x/10000",
        example = "20", required = true)
    maxFeeBips: Int,
    @ApiModelProperty(value = "label", example = "20", required = true)
    label: Long,
    @ApiModelProperty(value =
          "trading signature Rx of this order, decimal string", example =
          "13375450901292179417154974849571793069911517354720397125027633242680470075859",
        required = true)
    signatureRx: String,
    @ApiModelProperty(value =
          "trading signature Ry of this order, decimal string", example =
          "13375450901292179417154974849571793069911517354720397125027633242680470075859",
        required = true)
    signatureRy: String,
    @ApiModelProperty(value =
          "trading signature S of this order, decimal string", example =
          "13375450901292179417154974849571793069911517354720397125027633242680470075859",
        required = true)
    signatureS: String,
    @ApiModelProperty(value = "client specified ID of this order",
        example = "1")
    clientOrderId: Option[String] = None,
    @ApiModelProperty(value = "client specified channel ID of this order",
        example = "1")
    channelId: Option[String] = None)

object SubmitOrderRequest {
  implicit val format: Format[SubmitOrderRequest] = Json.format
}

@ApiModel(description = "API 结果对象")
case class ResultInfo(
    @ApiModelProperty(value = "返回码", example = "0", required = true)
    code: Int = 0,
    @ApiModelProperty(value = "返回信息", example = "SUCCESS", required = true)
    message: String = "SUCCESS")

object ResultInfo {
  implicit val format: Format[ResultInfo] = Json.format
}

@ApiModel(description = "获取市场深度响应对象")
case class GetDepthResponse(
    @ApiModelProperty(value = "返回结果", required = true)
    resultInfo: ResultInfo = ResultInfo(),
    @ApiModelProperty(value = "深度信息")
    depth: Option[Depth] = Some(Depth()))

object GetDepthResponse {
  implicit val format: Format[GetDepthResponse] = Json.format
}

@ApiModel(description = "下单响应对象")
case class SubmitOrderResponse(
    @ApiModelProperty(value = "返回结果", required = true)
    resultInfo: ResultInfo = ResultInfo())

object SubmitOrderResponse {
  implicit val format: Format[SubmitOrderResponse] = Json.format
}

@ApiModel(description = "深度信息")
case class Depth(
    @ApiModelProperty(value = "版本号信息", example = "147", required = true)
    version: Long = 1234,
    @ApiModelProperty(value = "时间戳", example = "432312312", required = true)
    timestamp: Long = 43232,
    @ApiModelProperty(value = "卖单深度", required = true)
    bids: List[Slot] = List(Slot()),
    @ApiModelProperty(value = "买单深度", required = true, dataType = "List[Int]")
    asks: List[Int] = List.empty[Int])

object Depth {
  implicit val format: Format[Depth] = Json.format
}

@ApiModel(description = "每一条深度数据")
case class Slot(
    @ApiModelProperty(value = "价格", example = "0.002", required = true)
    price: String = "0.002",
    @ApiModelProperty(value = "买方成交量", example = "21000", required = true)
    size: String = "21000",
    @ApiModelProperty(value = "卖方成交量", example = "33220000", required = true)
    volume: String = "332200000",
    @ApiModelProperty(value = "聚合的订单数目", example = "4", required = true)
    count: Int = 4)

object Slot {
  implicit val format: Format[Slot] = Json.format
}

/**
  * This controller creates an `Action` to handle HTTP requests to the
  * application's home page.
  */
@Singleton
@Api("{{api.desc}}")
class HomeController @Inject() (val controllerComponents: ControllerComponents)
    extends BaseController {

  @ApiOperation(
    value = "获取市场深度信息",
    notes = "获取某个市场对的深度信息。",
    code = 0,
    response = classOf[GetDepthResponse]
  )
  @ApiResponses(
    Array(
      new ApiResponse(code = 108000, message = "ERR_DEPTH_UNSUPPORTED_MARKET"),
      new ApiResponse(code = 108001, message = "ERR_DEPTH_UNSUPPORTED_LEVEL")
    )
  )
  def getDepth(
      @ApiParam(value = "市场对", required = true, example = "LRC-ETH")
      market: String,
      @ApiParam(value = "深度等级，越大表示合并的深度越多", required = true, example = "2")
      level: Int,
      @ApiParam(value = "返回条数限制", example = "2", defaultValue = "1")
      limit: Option[Int]
    ) = Action.async {
    Future.successful(Ok(Json.toJson(GetDepthResponse())))
  }

  @ApiOperation(
    value = "下订单",
    notes = "下买单或卖单。",
    code = 0,
    response = classOf[SubmitOrderResponse]
  )
  @ApiImplicitParams(
    Array(
      new ApiImplicitParam(
        value = "post submit order param body",
        required = true,
        dataType = "controllers.SubmitOrderRequest",
        paramType = "body"
      )
    )
  )
  @ApiResponses(
    Array(
      new ApiResponse(code = 102001, message = "ERR_EXCHANGE_ID_INVALID"),
      new ApiResponse(code = 102002, message = "ERR_TOKEN_ID_UNSUPPORT"),
      new ApiResponse(code = 102003, message = "ERR_ACCOUNT_ID_INVALID"),
      new ApiResponse(code = 102004, message = "ERR_ORDER_ID_INVALID"),
      new ApiResponse(code = 102005, message = "ERR_MARKET_UNSUPPORT"),
      new ApiResponse(code = 102006, message = "ERR_FEE_BIP_SETTING_UNSUPPORT"),
      new ApiResponse(code = 102007, message = "ERR_ORDER_EXIST"),
      new ApiResponse(code = 102008, message = "ERR_ORDER_EXPIRED"),
      new ApiResponse(code = 102009, message = "ERR_AMOUNT_S_TOO_SMALL"),
      new ApiResponse(code = 102010, message = "ERR_LACK_SIGN_INFO"),
      new ApiResponse(code = 102011, message = "ERR_BALANCE_NOT_ENOUGH"),
      new ApiResponse(code = 102012, message = "ERR_AMOUNT_LESS_THAN_DUST"),
      new ApiResponse(code = 102014, message = "ERR_FREEZE_BALANCE_FAILED"),
      new ApiResponse(code = 104001, message = "ERR_REST_EXPECT_APIKEY"),
      new ApiResponse(code = 104002, message = "ERR_REST_APIKEY_NOT_MATCH"),
      new ApiResponse(code = 104003, message = "ERR_REST_ACCOUNT_NOT_EXIST"),
      new ApiResponse(code = 104004, message = "ERR_REST_EXPECT_SIGNATURE"),
      new ApiResponse(code = 104005, message = "ERR_REST_INVALID_SIGNATURE")
    )
  )
  def submitOrder: Action[AnyContent] = Action.async { implicit request =>
    Future.successful(Ok(Json.toJson(SubmitOrderResponse())))
  }
}
