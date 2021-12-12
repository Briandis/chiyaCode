package com.test.mapper;

import java.util.List;
import chiya.core.base.page.Page;
import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;
import com.test.entity.User;
;
import com.test.entity.Topic;
;

@Mapper
public interface BaseReplyMapper {

	/**
	 * 添加回复内容
	 * 
	 * @param reply 回复内容
	 * @return 受影响行数
	 */
	Integer insertReply(Reply reply);

	/**
	 * 添加多个回复内容
	 * 
	 * @param list 回复内容列表
	 * @return 受影响行数
	 */
	Integer insertReplyList(@Param("list") List<Reply> list);

	/**
	 * 添加或更新回复内容，根据唯一性索引
	 * 
	 * @param list 回复内容列表
	 * @return 受影响行数
	 */
	Integer insertOrUpdateReplyByUnique(Reply reply);

	/**
	 * 添加或更新回复内容，根据查询条件
	 * 
	 * @param saveReply 添加的回复内容对象
	 * @param conditionReply 回复内容条件对象
	 * @return 受影响行数
	 */
	Integer insertOrUpdateReplyByWhere(@Param("saveReply") Reply saveReply, @Param("conditionReply") Reply conditionReply);

	/**
	 * 条件添加回复内容
	 * 
	 * @param saveReply 添加的回复内容对象
	 * @param conditionReply 回复内容条件对象
	 * @return 受影响行数
	 */
	Integer insertReplyByWhereOnlySave(@Param("saveReply") Reply saveReply, @Param("conditionReply") Reply conditionReply);

	/**
	 * 根据id真删回复内容
	 * 
	 * @param id 回复内容的id
	 * @return 受影响行数
	 */
	Integer deleteReplyById(Integer id);

	/**
	 * 根据id列表真删回复内容
	 * 
	 * @param list 回复内容的id列表
	 * @return 受影响行数
	 */
	Integer deleteReplyInId(List<Integer> list);

	/**
	 * 根据id和其他条件真删回复内容
	 * 
	 * @param id 回复内容的id
	 * @param reply 回复内容条件对象
	 * @return 受影响行数
	 */
	Integer deleteReplyByIdAndWhere(@Param("id") Integer id, @Param("reply") Reply reply);

	/**
	 * 根据条件真删回复内容
	 * 
	 * @param reply 回复内容条件对象
	 * @return 受影响行数
	 */
	Integer deleteReply(Reply reply);

	/**
	 * 根据id假删回复内容
	 * 
	 * @param id 回复内容的id
	 * @return 受影响行数
	 */
	Integer falseDeleteReplyById(Integer id);

	/**
	 * 根据id修改回复内容
	 * 
	 * @param reply 要更新的回复内容对象
	 * @return 受影响行数
	 */
	Integer updateReplyById(Reply reply);

	/**
	 * 根据id和不满足的条件更新回复内容，查询条件不满足时更新对象
	 * 
	 * @param saveReply 更新的回复内容对象
	 * @param conditionReply 不存在的回复内容对象
	 * @return 受影响行数
	 */
	Integer updateReplyByNotRepeatWhere(@Param("saveReply") Reply saveReply, @Param("conditionReply") Reply conditionReply);

	/**
	 * 根据id和其他的条件更新回复内容
	 * 
	 * @param saveReply 更新的回复内容对象
	 * @param conditionReply 回复内容条件对象
	 * @return 受影响行数
	 */
	Integer updateReplyByIdAndWhere(@Param("saveReply") Reply saveReply, @Param("conditionReply") Reply conditionReply);

	/**
	 * 根据条件更新回复内容
	 * 
	 * @param saveReply 更新的回复内容对象
	 * @param conditionReply 条件回复内容对象
	 * @return 受影响行数
	 */
	Integer updateReply(@Param("saveReply") Reply saveReply, @Param("conditionReply") Reply conditionReply);

	/**
	 * 记录id设置其他字段为null
	 * 
	 * @param reply 设置成null的回复内容对象，对象中字段不为Null则是要设置成null的字段
	 * @return 受影响行数
	 */
	Integer updateReplySetNullById(Reply reply);

	/**
	 * 根据id查询回复内容
	 * 
	 * @param id 回复内容的id
	 * @return 回复内容对象
	 */
	Reply selectReplyById(Integer id);

	/**
	 * 根据id列表查询回复内容
	 * 
	 * @param list 回复内容的id列表
	 * @return 回复内容对象列表
	 */
	List<Reply> selectReplyInId(List<Integer> list);

	/**
	 * 只查询一个回复内容
	 * 
	 * @param reply 回复内容对象
	 * @param index 获取的下标值
	 * @return 回复内容对象
	 */
	Reply selectOneReply(@Param("reply")Reply reply, @Param("index")Integer index);

	/**
	 * 查询多个回复内容
	 * 
	 * @param reply 回复内容对象
	 * @param page 分页对象
	 * @return 回复内容对象列表
	 */
	List<Reply> selectReply(@Param("reply")Reply reply, @Param("page") Page page);

	/**
	 * 统计回复内容记录数
	 * 
	 * @param reply 回复内容对象
	 * @return 查询到的记录数
	 */
	Integer countReply(@Param("reply")Reply reply);

	/**
	 * 内联一对一查询帖子
	 * 
	 * @param reply 回复内容对象
	 * @param topic 帖子对象
	 * @param page 分页对象
	 * @return 回复内容对象列表
	 */
	List<Reply> findReplyOneToOneTopic(@Param("reply") Reply reply, @Param("topic") Topic topic, @Param("page") Page page);

	/**
	 * 内联一对一统计帖子
	 * 
	 * @param reply 回复内容对象
	 * @param topic 帖子对象
	 * @return 查询到的记录数
	 */
	Integer countFindReplyOneToOneTopic(@Param("reply") Reply reply, @Param("topic") Topic topic);

	/**
	 * 内联一对一查询帖子，只返回帖子
	 * 
	 * @param reply 回复内容对象
	 * @param topic 帖子对象
	 * @param page 分页对象
	 * @return 查询到的记录数
	 */
	List<Topic> linkOneToOneTopic(@Param("reply") Reply reply, @Param("topic") Topic topic, @Param("page") Page page);

	/**
	 * 一对一查询帖子，只返回帖子
	 * 
	 * @param reply 回复内容对象
	 * @param topic 帖子对象
	 * @param page 分页对象
	 * @return 查询到的记录数
	 */
	List<Reply> queryReplyOneToOneTopic(@Param("reply") Reply reply, @Param("topic") Topic topic, @Param("page") Page page);

	/**
	 * 内联一对一查询用户表
	 * 
	 * @param reply 回复内容对象
	 * @param user 用户表对象
	 * @param page 分页对象
	 * @return 回复内容对象列表
	 */
	List<Reply> findReplyOneToOneUser(@Param("reply") Reply reply, @Param("user") User user, @Param("page") Page page);

	/**
	 * 内联一对一统计用户表
	 * 
	 * @param reply 回复内容对象
	 * @param user 用户表对象
	 * @return 查询到的记录数
	 */
	Integer countFindReplyOneToOneUser(@Param("reply") Reply reply, @Param("user") User user);

	/**
	 * 内联一对一查询用户表，只返回用户表
	 * 
	 * @param reply 回复内容对象
	 * @param user 用户表对象
	 * @param page 分页对象
	 * @return 查询到的记录数
	 */
	List<User> linkOneToOneUser(@Param("reply") Reply reply, @Param("user") User user, @Param("page") Page page);

	/**
	 * 一对一查询用户表，只返回用户表
	 * 
	 * @param reply 回复内容对象
	 * @param user 用户表对象
	 * @param page 分页对象
	 * @return 查询到的记录数
	 */
	List<Reply> queryReplyOneToOneUser(@Param("reply") Reply reply, @Param("user") User user, @Param("page") Page page);

}